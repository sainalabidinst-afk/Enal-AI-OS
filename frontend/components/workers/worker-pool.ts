export function createWorker(workerPath: string) {
  if (typeof window === "undefined" || !window.Worker) {
    return null;
  }

  try {
    return new Worker(workerPath, { type: "module" });
  } catch (error) {
    console.error(`Failed to create worker: ${workerPath}`, error);
    return null;
  }
}

export interface WorkerTask<T, R> {
  id: string;
  payload: T;
  resolve: (result: R) => void;
  reject: (error: Error) => void;
}

export class WorkerPool {
  private workers: Worker[] = [];
  private taskQueue: WorkerTask<unknown, unknown>[] = [];
  private activeTasks = new Map<string, WorkerTask<unknown, unknown>>();
  private workerPaths: string[] = [];

  constructor(workerPaths: string[]) {
    this.workerPaths = workerPaths;
  }

  initialize(poolSize = 2) {
    for (let i = 0; i < poolSize; i++) {
      const workerPath = this.workerPaths[i % this.workerPaths.length];
      const worker = createWorker(workerPath);
      if (worker) {
        this.workers.push(worker);
        worker.onmessage = (e) => {
          const { id, result, error } = e.data;
          const task = this.activeTasks.get(id);
          if (task) {
            if (error) {
              task.reject(new Error(error));
            } else {
              task.resolve(result);
            }
            this.activeTasks.delete(id);
          }
          this.processNext();
        };
      }
    }
  }

  async execute<T, R>(payload: T): Promise<R> {
    return new Promise((resolve, reject) => {
      const task: WorkerTask<T, R> = {
        id: `task-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
        payload,
        resolve: resolve as (result: unknown) => void,
        reject: reject as (error: Error) => void,
      };

      const availableWorker = this.workers.find((w) => {
        const isBusy = Array.from(this.activeTasks.values()).some((t) => t.id.startsWith(`task-`));
        return !isBusy;
      });

      if (availableWorker) {
        this.sendTask(availableWorker, task as WorkerTask<unknown, unknown>);
      } else {
        this.taskQueue.push(task as WorkerTask<unknown, unknown>);
      }
    });
  }

  dispose() {
    this.workers.forEach((worker) => worker.terminate());
    this.workers = [];
    this.taskQueue = [];
    this.activeTasks.clear();
  }

  private sendTask(worker: Worker, task: WorkerTask<unknown, unknown>) {
    this.activeTasks.set(task.id, task);
    worker.postMessage({
      id: task.id,
      type: "indicator",
      payload: task.payload,
    });
  }

  private processNext() {
    if (this.taskQueue.length === 0) return;

    const task = this.taskQueue.shift();
    if (!task) return;

    const availableWorker = this.workers[0];
    if (availableWorker) {
      this.sendTask(availableWorker, task);
    }
  }
}
