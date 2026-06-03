import { describe, it, expect } from 'vitest';
import { cn } from './cn';

describe('cn utility', () => {
  it('should merge tailwind classes properly', () => {
    expect(cn('p-2', 'p-4')).toBe('p-4');
  });

  it('should handle conditional classes', () => {
    const isRed = true;
    const isBlue = false;
    expect(cn('p-2', isRed && 'text-red-500', isBlue && 'text-blue-500')).toBe('p-2 text-red-500');
  });

  it('should handle arrays and nested arrays', () => {
    expect(cn(['p-2', 'text-sm'], [['font-bold', 'text-red-500']])).toBe('p-2 text-sm font-bold text-red-500');
  });

  it('should handle objects with conditional classes', () => {
    expect(cn({ 'p-2': true, 'p-4': false, 'text-sm': true })).toBe('p-2 text-sm');
  });

  it('should resolve conflicts appropriately (tailwind-merge)', () => {
    expect(cn('px-2 py-1', 'p-4')).toBe('p-4');
    expect(cn('p-4', 'px-2 py-1')).toBe('p-4 px-2 py-1');
  });

  it('should handle falsy values', () => {
    expect(cn('p-2', null, undefined, false, 0, '')).toBe('p-2');
  });
});
