export class Utils {
  static getURL(p: string): string {
    return new URL(p, process.env.REACT_APP_URL).href;
  }
}
