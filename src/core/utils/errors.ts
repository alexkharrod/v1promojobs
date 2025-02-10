export class CustomError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CustomError";
  }
}

export function handleError(error: Error) {
  console.error(error);
  // Implement error logging and reporting here
}
