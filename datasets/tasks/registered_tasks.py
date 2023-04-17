from datasets.tasks.existence_task import ExistenceTask
from datasets.tasks.count_task import CountTask
from datasets.tasks.transitivity_task import TransitivityTask
from datasets.tasks.coordinate_task import CoordinateTask
from datasets.tasks.existence_tracking_task import ExistenceTrackingTask 
 
tasks = [
    ExistenceTask("existence"),
    CountTask("count"),
    TransitivityTask("transitivity"),
    CoordinateTask("coordinate"),
    ExistenceTrackingTask("existence_tracking")
]