import fs from 'fs';
import path from 'path';
const dir = path.join(process.cwd(), 'content');
export function read(name){ try { return fs.readFileSync(path.join(dir, name), 'utf8'); } catch { return ''; } }
export function readJSON(name){ try { return JSON.parse(read(name) || '[]'); } catch { return []; } }
