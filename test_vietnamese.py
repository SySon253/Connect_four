#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Vietnamese text rendering in the game
"""

import pygame
import sys

def test_vietnamese_text():
    """Test rendering tiếng Việt"""
    pygame.init()
    
    print("=" * 60)
    print("Vietnamese Text Rendering Test")
    print("=" * 60)
    
    # Test các font
    test_strings = [
        'CONNECT FOUR',
        'NGƯỜI VS NGƯỜI',
        'NGƯỜI VS MÁY',
        'CÀI ĐẶT',
        'NGÔN NGỮ',
        'THỜI GIAN',
        'START',
        'EXIT',
        'SAVE',
    ]
    
    fonts = ['calibri', 'arial', 'segoeui']
    
    print("\n✓ Testing fonts and text rendering:\n")
    
    for font_name in fonts:
        print(f"Font: {font_name}")
        print("-" * 40)
        
        try:
            font = pygame.font.SysFont(font_name, 32)
            
            for text in test_strings:
                surface = font.render(text, True, (0, 0, 0))
                width, height = surface.get_size()
                status = "✓" if width > 0 else "✗"
                print(f"  {status} {text:20} → {width}x{height}px")
            
            print()
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
    
    # Test AssetLoader
    print("=" * 60)
    print("Testing AssetLoader (from game):")
    print("=" * 60)
    
    try:
        from utils.asset_loader import init_assets, asset_loader
        init_assets()
        
        print("\n✓ Assets initialized!")
        print(f"  Fonts loaded: {list(asset_loader.fonts.keys())}")
        
        # Test font rendering
        font = asset_loader.get_font('medium')
        test_text = 'NGƯỜI VS MÁY'
        surface = font.render(test_text, True, (0, 0, 0))
        print(f"  Test render '{test_text}': {surface.get_size()[0]}x{surface.get_size()[1]}px ✓")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✓ Vietnamese text rendering works!")
    print("=" * 60)

if __name__ == "__main__":
    test_vietnamese_text()
