import { useState } from 'react';
import { Task } from '../utils/data-tasks';

const TaskCard = ({ task, updateTask, deleteTask }: {
  task: Task;
  updateTask: (task: Task) => void;
  deleteTask: (taskId: string) => void;
}) => {

  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [title, setTitle] = useState(task.title);

  const handleBlur = () => {
    if (title !== task.title) {
      updateTask({ ...task, title });
    }
    setIsEditingTitle(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
  };

  return (
    <div
      draggable
      onDragStart={(e) => {
        e.dataTransfer.setData("taskId", task.taskId);
      }}
      className="border rounded-lg px-2 m-2 bg-gray-50 w-56"
    >
      <div className="text-base font-base py-2">
        {isEditingTitle ? (
          <input
            autoFocus
            className="w-full"
            onBlur={handleBlur}
            value={title}
            onChange={handleChange}
          />
        ) : (
          <div onClick={() => {
            setTitle(task.title);
            setIsEditingTitle(true);
          }}>
            {title}
          </div>
        )}
      </div>
      <div className="flex gap-4 justify-between py-2 text-gray-500 text-sm">
        <div className="flex gap-2">
          <div>#{task.taskId}</div>
        </div>

        <div className="flex gap-2 items-center">
          <div className="font-bold">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              className="bi bi-trash"
              viewBox="0 0 16 16"
              onClick={() => deleteTask(task.taskId)} 
              style={{ cursor: 'pointer' }}
            >
              <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z" />
              <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1 1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z" />
            </svg>
          </div>
        </div>

      </div>
    </div>
  );
};

export default TaskCard;
