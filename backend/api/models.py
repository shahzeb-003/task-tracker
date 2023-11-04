from django.db import models


#Create a Task database table that has the columns title, due_date, priority and email.
class Task(models.Model):

    """Create a Task database table that has the columns title, due_date, priority, and email."""

    title = models.CharField(max_length=100)
    due_date = models.DateField()
    priority = models.IntegerField()
    email = models.EmailField()

    #returns the title of the Task
    def __str__(self) :
        """Return the title of the Task."""

        return self.title
    
    def to_dict(self):
        """Convert the Task object to a dictionary."""
        
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date,
            'priority': self.priority,
            'email': self.email
        }