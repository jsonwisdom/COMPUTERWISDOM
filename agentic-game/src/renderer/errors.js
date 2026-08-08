export class RendererError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'RendererError';
    this.code = code;
  }
}
