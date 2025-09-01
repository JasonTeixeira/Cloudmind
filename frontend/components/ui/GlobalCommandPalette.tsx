'use client';

import React from 'react';
import CommandPalette, { useCommandPalette } from './CommandPalette';

export function GlobalCommandPalette() {
  const { isOpen, close } = useCommandPalette();
  
  return <CommandPalette isOpen={isOpen} onClose={close} />;
}
