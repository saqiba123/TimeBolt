from collections import defaultdict
import datetime
import time
import csv
import os
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import TrackerModel
from .serializers import TrackerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.timezone import now, localtime
import json
from rest_framework import status
#api to start a task
import pytz
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required


PAKISTAN_TZ = pytz.timezone("Asia/Karachi")


def welcome(request):
    return render(request, 'tracker/welcome.html')

@login_required
def home(request):
    user = request.user
    
    ongoing_tasks = TrackerModel.objects.filter(user=user,end_time__isnull=True)  # Show only ongoing tasks
    completed_tasks = TrackerModel.objects.filter(user=user,end_time__isnull=False)  # Show completed tasks with duration
    
     # Format duration as HH:MM:SS before passing it to the template
    for task in completed_tasks:
        if task.duration:
            total_seconds = int(task.duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            task.formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            task.formatted_duration = "00:00:00"
    
    # Calculate daily work hours
    daily_work = defaultdict(timedelta)  # Stores work duration per day
    daily_tasks = defaultdict(list)
    for task in completed_tasks:
        task_date = localtime(task.end_time).date()  # Convert to local date
        daily_work[task_date] += task.duration
        daily_tasks[task_date].append(
            f"{task.task_name} - Duration: {task.formatted_duration}")
    # Prepare data for the last 5 days
    labels = []
    durations = []
    work_data = {}

    for i in range(5):
        day = now().date() - timedelta(days=i)
        formatted_day = day.strftime("%b %d")
        total_time = daily_work[day]  # Fix key reference
        total_seconds = int(total_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_work = hours * 60 + minutes  # Convert to minutes
        labels.append(formatted_day)
        durations.append(formatted_work)
        work_data[formatted_day] = daily_tasks[day]  # Fix reference to correct key
    # Convert `work_data` to JSON
    work_data_json = json.dumps(work_data, ensure_ascii=False)
    #=================================================================================================================
    new_today = timezone.now().date()
    # Get completed tasks for today (tasks with end_time)
    completed_tasks = TrackerModel.objects.filter(user=request.user,end_time__date=new_today,end_time__isnull=False)
    # Get total worked time from duration field
    total_work_seconds = sum(task.duration.total_seconds() for task in completed_tasks if task.duration is not None)
    # Format hours and minutes
    hours = int(total_work_seconds // 3600)
    minutes = int((total_work_seconds % 3600) // 60)
    worked_hours = f"{hours}h {minutes}m"
    # Calculate breaks (time between consecutive tasks)
    all_tasks = list(completed_tasks.order_by('start_time'))
    break_seconds = 0
    # Count tasks today
    tasks_count = completed_tasks.count()
    #last three completed tasks:
    latest_completed_tasks = TrackerModel.objects.all().order_by('-id')[:3]  # Get latest 3 tasks
    latest_task_names = [task.task_name for task in latest_completed_tasks]  # Assuming 'name' is the task field
    
    def generate_summary(tasks, worked_hours):
        if not tasks:
            return "You haven’t completed any tasks today. Let’s get started!"
        
        task_names = [task.task_name for task in tasks]
        summary = f"You completed {len(tasks)} task(s) today"
        
        if len(task_names) > 0:
            task_list = ", ".join(task_names[:3])
            summary += f" including '{task_list}'"
            if len(task_names) > 3:
                summary += " and more"
            summary += "."
        
        summary += f" Total work time was {worked_hours}. Great job!"
        return summary

    day_summary = generate_summary(completed_tasks, worked_hours)

    
    
    
    
    return render(request, "tracker/index.html", {
                'worked_hours': worked_hours,
                'tasks_count': tasks_count,
                'latest_task_names':latest_task_names,
                "tasks": ongoing_tasks,
                "completed_tasks": completed_tasks,
                "labels": labels,
                "durations": durations,
                "work_data": work_data_json,  # Pass JSON-safe data
                "day_summary": day_summary
            })
class TasksByDateAPI(APIView):
    def get(self, request):
        selected_date = request.GET.get("date")  # Get date from frontend
        if selected_date is not None:
            try:
                date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
                # Get tasks completed on this date
                tasks = TrackerModel.objects.filter(user=request.user,end_time__date=date_obj)
                task_list = [{
                        "task_name": task.task_name,
                        "duration": str(task.duration) if task.duration else "00:00:00",
                        "end_time": localtime(task.end_time, PAKISTAN_TZ).strftime("%Y-%m-%d %H:%M:%S")}
                    for task in tasks]
                return Response({"tasks": task_list}, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class StartTaskAPI(APIView):
    @swagger_auto_schema(
        operation_description="Start new task",
        request_body= openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"task_name":openapi.Schema(type=openapi.TYPE_STRING, description="Task Name")},
            required=["task_name"]),
        responses={200: "Task started successfully"})
    
    def post(self, request):
        task_name = request.data.get("task_name")
        task = TrackerModel.objects.create(task_name=task_name, user=request.user) # to associate task with current user
        return redirect("home") 
        
class EndTaskAPI(APIView):
    @swagger_auto_schema(
        operation_description="Task End",
        responses={200: "Task ended successfully"}
    )
    
    def post(self,request,task_id):
        try:
            task = TrackerModel.objects.get(id= task_id,user=request.user)
            if task.end_time is None:
                # task.end_time = datetime.now()
                task.end_time = now()  # Ensure it's timezone-aware
                task.duration = task.end_time - task.start_time
                task.save()
                 # Convert duration to HH:MM:SS format
                formatted_duration = str(timedelta(seconds=task.duration.total_seconds())).split(".")[0]
                
                  # Fetch updated tasks
                ongoing_tasks = TrackerModel.objects.filter(user=request.user,end_time__isnull=True)
                completed_tasks = TrackerModel.objects.filter(user=request.user,end_time__isnull=False)
 
                request.session["message"] = f"Task '{task.task_name}' ended! Duration: {formatted_duration}"
                return redirect("home")
                # return Response({"message":"Task ended","duration":str(task.duration)})
            return Response({"message": "Task already ended"}, status=400)
        except TrackerModel.DoesNotExist:
            return Response({"message":"Task not found!"},status=404)

class ExportTasksCSV(APIView):
    @swagger_auto_schema(
        operation_description="Export today's tasks to a CSV file",
        responses={200: "CSV exported successfully"})
    
    def get(self,request):
        today_date = datetime.now().strftime("%Y-%m-%d")
        file_name = f"sheet_{request.user.username}_{today_date}.csv"
        tasks = TrackerModel.objects.filter(user=request.user,start_time__date=today_date)
        file_exist = os.path.isfile(file_name)
        if not tasks.exists():
            return Response({"message":"Task not found!"},status=404)
        with open(file_name,mode="a",newline="") as file:
            writer = csv.writer(file)
            if not file_exist:
                writer.writerow(["TaskName", "StartedTime","EndedTime","DurationTime"])
            for task in tasks:
                writer.writerow([task.task_name,task.start_time,task.end_time,task.duration])
        
        return Response({"message":f"CSV exported: {file_name}"})
            

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
