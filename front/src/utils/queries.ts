import { gql } from '@apollo/client';

export const GET_TASKS = gql`
  query GetTasks {
    tasks {
      tasks {
        taskId
        title
        status
      }
    }
  }
`;

export const CREATE_TASK = gql`
  mutation CreateTask($taskId: String!, $title: String!, $status: String!) {
    createTask(taskId: $taskId, title: $title, status: $status) {
      taskId
      title
      status
    }
  }
`;

export const UPDATE_TASK = gql`
  mutation UpdateTask($taskId: String!, $title: String, $status: String) {
    updateTask(taskId: $taskId, title: $title, status: $status) {
      taskId
      title
      status
    }
  }
`;

export const DELETE_TASK = gql`
  mutation DeleteTask($taskId: String!) {
    deleteTask(taskId: $taskId)
  }
`;


