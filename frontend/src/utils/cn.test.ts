import { describe, it, expect } from 'vitest';
import { cn } from './cn';

describe('cn utility function', () => {
  it('merges basic class names correctly', () => {
    expect(cn('class-a', 'class-b')).toBe('class-a class-b');
  });

  it('resolves tailwind conflicts using tailwind-merge', () => {
    // text-red-500 should be overridden by text-blue-500
    expect(cn('text-red-500', 'text-blue-500')).toBe('text-blue-500');
    // px-2 should be overridden by p-4 which includes px
    expect(cn('px-2', 'p-4')).toBe('p-4');
  });

  it('handles conditional classes correctly', () => {
    const isTrue = true;
    const isFalse = false;
    expect(cn('base-class', isTrue && 'active-class', isFalse && 'hidden-class')).toBe('base-class active-class');
  });

  it('handles arrays of classes', () => {
    expect(cn(['class-a', 'class-b'], 'class-c')).toBe('class-a class-b class-c');
  });

  it('handles objects with boolean values', () => {
    expect(cn({ 'class-a': true, 'class-b': false, 'class-c': true })).toBe('class-a class-c');
  });

  it('handles undefined, null and empty inputs gracefully', () => {
    expect(cn('class-a', undefined, null, '', false)).toBe('class-a');
    expect(cn()).toBe('');
  });
});
