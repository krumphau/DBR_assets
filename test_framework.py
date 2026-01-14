#!/usr/bin/env python3
"""
DBR TTS Save File Test Framework
=================================

This framework validates TTS save files and assets to ensure:
1. Correct table dimensions and properties
2. All assets placed neatly on tables
3. Terrain sized appropriately for DBR gameplay
4. All constraints and requirements met

Run after EVERY change to verify correctness.
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class Color:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TTSTestFramework:
    """Test framework for validating DBR TTS save files"""
    
    def __init__(self, save_file_path: str):
        self.save_file_path = save_file_path
        self.save_data = None
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Expected configuration (from Memory ID: 13378506)
        self.EXPECTED_MAIN_TABLE = {
            'position': {'x': 0.0, 'y': 1.0, 'z': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0},
            'name': 'Custom_Model'
        }
        
        self.EXPECTED_LEFT_TABLE = {
            'position': {'x': -40.0, 'y': 1.0, 'z': 0.0},
            'scale': {'x': 15.0, 'y': 1.0, 'z': 40.0},
            'name': 'BlockSquare'
        }
        
        self.EXPECTED_RIGHT_TABLE = {
            'position': {'x': 40.0, 'y': 1.0, 'z': 0.0},
            'scale': {'x': 15.0, 'y': 1.0, 'z': 40.0},
            'name': 'BlockSquare'
        }
        
        # Unit scale for 40mm bases
        self.UNIT_SCALE = 0.039
        self.UNIT_SCALE_TOLERANCE = 0.001
        
        # Hill scales (rescaled for visibility)
        self.HILL_SCALES = {
            'small': 0.15,
            'medium': 0.20,
            'large': 0.28
        }
        self.HILL_SCALE_TOLERANCE = 0.01
        
        # Terrain scale ranges
        self.TERRAIN_SCALE_MIN = 0.06
        self.TERRAIN_SCALE_MAX = 0.12
        
        # Table bounds for neat placement checks
        self.RIGHT_TABLE_BOUNDS = {
            'x_min': 30.0, 'x_max': 50.0,
            'z_min': -25.0, 'z_max': 25.0,
            'y': 2.0
        }
        
    def load_save_file(self) -> bool:
        """Load and parse the save file"""
        try:
            with open(self.save_file_path, 'r') as f:
                self.save_data = json.load(f)
            self.info.append(f"✓ Loaded save file: {os.path.basename(self.save_file_path)}")
            return True
        except FileNotFoundError:
            self.errors.append(f"✗ Save file not found: {self.save_file_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"✗ Invalid JSON: {e}")
            return False
    
    def test_save_metadata(self):
        """Test 1: Validate save file metadata"""
        print(f"\n{Color.BOLD}Test 1: Save File Metadata{Color.END}")
        
        # Check SaveName has timestamp
        save_name = self.save_data.get('SaveName', '')
        if not save_name:
            self.errors.append("✗ Missing SaveName field")
        elif ' - ' not in save_name or not any(char.isdigit() for char in save_name[-20:]):
            self.warnings.append("⚠ SaveName may be missing timestamp")
        else:
            self.info.append(f"✓ SaveName: {save_name}")
        
        # Check ObjectStates exists
        if 'ObjectStates' not in self.save_data:
            self.errors.append("✗ Missing ObjectStates array")
            return
        
        obj_count = len(self.save_data['ObjectStates'])
        self.info.append(f"✓ Total objects: {obj_count}")
        
        if obj_count < 35:
            self.warnings.append(f"⚠ Low object count: {obj_count} (expected 40+)")
    
    def test_table_configuration(self):
        """Test 2: Validate table dimensions and properties"""
        print(f"\n{Color.BOLD}Test 2: Table Configuration{Color.END}")
        
        tables = {
            'main': None,
            'left': None,
            'right': None
        }
        
        for obj in self.save_data['ObjectStates']:
            nickname = obj.get('Nickname', '').lower()
            if 'main' in nickname and 'table' in nickname:
                tables['main'] = obj
            elif 'left' in nickname and 'table' in nickname:
                tables['left'] = obj
            elif 'right' in nickname and 'table' in nickname:
                tables['right'] = obj
        
        # Check main table
        if not tables['main']:
            self.errors.append("✗ Main table not found")
        else:
            self._validate_table(tables['main'], self.EXPECTED_MAIN_TABLE, "Main")
        
        # Check left table
        if not tables['left']:
            self.errors.append("✗ Left side table not found")
        else:
            self._validate_table(tables['left'], self.EXPECTED_LEFT_TABLE, "Left")
        
        # Check right table
        if not tables['right']:
            self.errors.append("✗ Right side table not found")
        else:
            self._validate_table(tables['right'], self.EXPECTED_RIGHT_TABLE, "Right")
    
    def _validate_table(self, table: Dict, expected: Dict, name: str):
        """Validate a single table configuration"""
        transform = table.get('Transform', {})
        
        # Check position
        pos_x = transform.get('posX', 0)
        pos_y = transform.get('posY', 0)
        pos_z = transform.get('posZ', 0)
        
        exp_pos = expected['position']
        if abs(pos_x - exp_pos['x']) > 0.1 or abs(pos_y - exp_pos['y']) > 0.1 or abs(pos_z - exp_pos['z']) > 0.1:
            self.errors.append(f"✗ {name} table position incorrect: ({pos_x}, {pos_y}, {pos_z}) != ({exp_pos['x']}, {exp_pos['y']}, {exp_pos['z']})")
        else:
            self.info.append(f"✓ {name} table position correct")
        
        # Check scale
        scale_x = transform.get('scaleX', 1)
        scale_y = transform.get('scaleY', 1)
        scale_z = transform.get('scaleZ', 1)
        
        exp_scale = expected['scale']
        if abs(scale_x - exp_scale['x']) > 0.1 or abs(scale_y - exp_scale['y']) > 0.1 or abs(scale_z - exp_scale['z']) > 0.1:
            self.errors.append(f"✗ {name} table scale incorrect: ({scale_x}, {scale_y}, {scale_z}) != ({exp_scale['x']}, {exp_scale['y']}, {exp_scale['z']})")
        else:
            self.info.append(f"✓ {name} table scale correct")
        
        # Check locked
        if name == "Main" and not table.get('Locked', False):
            self.warnings.append(f"⚠ {name} table should be locked")
    
    def test_asset_placement(self):
        """Test 3: Validate asset placement on tables"""
        print(f"\n{Color.BOLD}Test 3: Asset Placement{Color.END}")
        
        units_on_table = []
        units_off_table = []
        
        for obj in self.save_data['ObjectStates']:
            if obj.get('Name') == 'Custom_AssetBundle':
                nickname = obj.get('Nickname', '')
                
                # Skip terrain (in bag) and tools
                if any(word in nickname.lower() for word in ['terrain', 'tool']):
                    continue
                
                transform = obj.get('Transform', {})
                x = transform.get('posX', 0)
                z = transform.get('posZ', 0)
                y = transform.get('posY', 0)
                
                # Check if on right side table
                bounds = self.RIGHT_TABLE_BOUNDS
                if (bounds['x_min'] <= x <= bounds['x_max'] and 
                    bounds['z_min'] <= z <= bounds['z_max'] and
                    abs(y - bounds['y']) < 0.5):
                    units_on_table.append(nickname)
                else:
                    units_off_table.append((nickname, x, y, z))
        
        self.info.append(f"✓ Units on right table: {len(units_on_table)}")
        
        if units_off_table:
            self.warnings.append(f"⚠ Units off table or falling: {len(units_off_table)}")
            for name, x, y, z in units_off_table[:5]:  # Show first 5
                self.warnings.append(f"  - {name} at ({x:.1f}, {y:.1f}, {z:.1f})")
    
    def test_unit_scaling(self):
        """Test 4: Validate unit scaling (40mm bases)"""
        print(f"\n{Color.BOLD}Test 4: Unit Scaling{Color.END}")
        
        incorrectly_scaled = []
        correctly_scaled = 0
        
        for obj in self.save_data['ObjectStates']:
            if obj.get('Name') == 'Custom_AssetBundle':
                nickname = obj.get('Nickname', '')
                
                # Skip terrain
                if 'terrain' in nickname.lower():
                    continue
                
                transform = obj.get('Transform', {})
                scale = transform.get('scaleX', 0)
                
                if abs(scale - self.UNIT_SCALE) > self.UNIT_SCALE_TOLERANCE:
                    incorrectly_scaled.append((nickname, scale))
                else:
                    correctly_scaled += 1
        
        self.info.append(f"✓ Correctly scaled units: {correctly_scaled}")
        
        if incorrectly_scaled:
            self.errors.append(f"✗ Incorrectly scaled units: {len(incorrectly_scaled)}")
            for name, scale in incorrectly_scaled[:5]:  # Show first 5
                self.errors.append(f"  - {name}: {scale:.4f} (expected {self.UNIT_SCALE})")
    
    def test_terrain_scaling(self):
        """Test 5: Validate terrain scaling based on ACTUAL PHYSICAL SIZE in DBR rules"""
        print(f"\n{Color.BOLD}Test 5: Terrain Scaling (Physical Size){Color.END}")
        
        # DBR terrain size rules (in feet on 6x4 table)
        # These are the ACTUAL physical dimensions after scale is applied
        DBR_TERRAIN_SIZES = {
            # Area terrain (organic boundaries)
            'bua_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},  # 6-12 inches
            'bua_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},  # 9-18 inches
            'bua_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},  # 12-24 inches
            
            'wood_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},
            'wood_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},
            'wood_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},
            
            'marsh_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},
            'marsh_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},
            'marsh_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},
            
            'hill_gentle_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},
            'hill_gentle_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},
            'hill_gentle_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},
            
            'hill_steep_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},
            'hill_steep_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},
            'hill_steep_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},
            
            'ploughedfield_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},
            'ploughedfield_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},
            'ploughedfield_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},
            
            'rockyground_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},
            'rockyground_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},
            'rockyground_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},
            
            'enclosure_small': {'min': 0.5, 'max': 1.0, 'typical': 0.75},
            'enclosure_medium': {'min': 0.75, 'max': 1.5, 'typical': 1.0},
            'enclosure_large': {'min': 1.0, 'max': 2.0, 'typical': 1.5},
            
            # Linear terrain
            'river': {'min': 0.25, 'max': 1.0, 'typical': 0.5},  # 3-12 inches wide
            'stream': {'min': 0.1, 'max': 0.5, 'typical': 0.25},  # 1-6 inches wide
            'road': {'min': 0.15, 'max': 0.5, 'typical': 0.25},  # 2-6 inches wide
            'ford': {'min': 0.25, 'max': 0.75, 'typical': 0.5},
            'pond': {'min': 0.5, 'max': 1.5, 'typical': 1.0},
            'lake': {'min': 1.0, 'max': 3.0, 'typical': 2.0},
            
            # Fortifications
            'fortification': {'min': 0.5, 'max': 2.0, 'typical': 1.0},
            
            # Waterway features (4 feet long × 0.5-2 feet wide coastline)
            'waterway': {'min': 2.0, 'max': 6.0, 'typical': 4.0},  # Length (up to 6 feet for large features)
            'coastline': {'min': 2.0, 'max': 6.0, 'typical': 4.0},  # Same as waterway
        }
        
        # Estimated base dimensions for different terrain types (in TTS units before scale)
        # These are rough estimates - the actual check is against final physical size
        TERRAIN_BASE_SIZES = {
            'default': 100.0,  # Most terrain models are ~100 units base size
            'waterway': 100.0,  # Coastline waterway base is ~100 units (4 feet at scale 4.0)
            'coastline': 100.0,  # Same as waterway
        }
        
        terrain_pieces = []
        terrain_correct = []
        terrain_too_small = []
        terrain_too_large = []
        
        for obj in self.save_data['ObjectStates']:
            # Check in bags too
            if obj.get('Name') == 'Bag':
                for contained in obj.get('ContainedObjects', []):
                    if contained.get('Name') == 'Custom_AssetBundle':
                        nickname = contained.get('Nickname', '')
                        if 'terrain' in nickname.lower():
                            scale = contained.get('Transform', {}).get('scaleX', 0)
                            terrain_pieces.append((nickname, scale, contained))
            
            # Check loose terrain
            if obj.get('Name') == 'Custom_AssetBundle':
                nickname = obj.get('Nickname', '')
                if 'terrain' in nickname.lower():
                    scale = obj.get('Transform', {}).get('scaleX', 0)
                    terrain_pieces.append((nickname, scale, obj))
        
        # Check terrain physical sizes
        for name, scale, obj in terrain_pieces:
            name_lower = name.lower().replace(' ', '').replace('terrain', '')
            
            # Determine terrain type and size
            terrain_key = None
            base_size = TERRAIN_BASE_SIZES['default']
            
            # Match terrain type
            for key in DBR_TERRAIN_SIZES.keys():
                key_parts = key.split('_')
                # Check if all parts of key are in the name
                if all(part in name_lower for part in key_parts):
                    terrain_key = key
                    break
            
            # Special case for waterways
            if 'waterway' in name_lower or 'coastline' in name_lower:
                terrain_key = 'waterway'
                base_size = TERRAIN_BASE_SIZES['waterway']
            
            # If we found a matching terrain type, validate size
            if terrain_key:
                size_rules = DBR_TERRAIN_SIZES[terrain_key]
                
                # Calculate physical size in feet (TTS scale * base_size / 100)
                # Approximate conversion: 100 TTS units ≈ 1 foot at scale 1.0
                physical_size = scale * base_size / 100.0
                
                min_size = size_rules['min']
                max_size = size_rules['max']
                
                if physical_size < min_size:
                    terrain_too_small.append((name, scale, physical_size, min_size, max_size))
                elif physical_size > max_size:
                    terrain_too_large.append((name, scale, physical_size, min_size, max_size))
                else:
                    terrain_correct.append((name, scale, physical_size))
            else:
                # Unknown terrain type - just check it's reasonable
                physical_size = scale * base_size / 100.0
                if 0.1 <= physical_size <= 3.0:  # Between 1 inch and 3 feet
                    terrain_correct.append((name, scale, physical_size))
                else:
                    self.warnings.append(f"⚠ {name}: unusual size {physical_size:.2f} feet (scale {scale:.3f})")
        
        self.info.append(f"✓ Total terrain pieces: {len(terrain_pieces)}")
        self.info.append(f"✓ Correctly sized terrain: {len(terrain_correct)}")
        
        if terrain_too_small:
            self.errors.append(f"✗ Terrain pieces TOO SMALL for DBR: {len(terrain_too_small)}")
            for name, scale, phys, min_s, max_s in terrain_too_small[:5]:
                self.errors.append(f"  - {name}: {phys:.2f}ft (scale {scale:.3f}) < min {min_s:.2f}ft")
        
        if terrain_too_large:
            self.errors.append(f"✗ Terrain pieces TOO LARGE for DBR: {len(terrain_too_large)}")
            for name, scale, phys, min_s, max_s in terrain_too_large[:5]:
                self.errors.append(f"  - {name}: {phys:.2f}ft (scale {scale:.3f}) > max {max_s:.2f}ft")
    
    def test_github_urls(self):
        """Test 6: Validate all assets use GitHub URLs"""
        print(f"\n{Color.BOLD}Test 6: GitHub URLs{Color.END}")
        
        local_urls = []
        github_urls = 0
        
        def check_urls(obj):
            # Check AssetBundles
            if obj.get('Name') == 'Custom_AssetBundle':
                url = obj.get('CustomAssetbundle', {}).get('AssetbundleURL', '')
                if url:
                    if url.startswith('http') and 'github' in url:
                        return 'github'
                    else:
                        return ('local', obj.get('Nickname', 'Unknown'), url)
            
            # Check Custom Models (tables)
            if obj.get('Name') == 'Custom_Model':
                mesh_url = obj.get('CustomMesh', {}).get('MeshURL', '')
                diff_url = obj.get('CustomMesh', {}).get('DiffuseURL', '')
                
                results = []
                if mesh_url:
                    if 'github' in mesh_url:
                        results.append('github')
                    else:
                        results.append(('local', obj.get('Nickname', 'Table'), mesh_url))
                
                if diff_url:
                    if 'github' in diff_url:
                        results.append('github')
                    else:
                        results.append(('local', obj.get('Nickname', 'Table'), diff_url))
                
                return results if results else None
            
            return None
        
        for obj in self.save_data['ObjectStates']:
            result = check_urls(obj)
            if result:
                if isinstance(result, list):
                    for r in result:
                        if r == 'github':
                            github_urls += 1
                        else:
                            local_urls.append(r[1:])  # name, url
                elif result == 'github':
                    github_urls += 1
                elif result[0] == 'local':
                    local_urls.append(result[1:])  # name, url
            
            # Check in bags
            if obj.get('Name') == 'Bag':
                for contained in obj.get('ContainedObjects', []):
                    result = check_urls(contained)
                    if result == 'github':
                        github_urls += 1
                    elif result and result[0] == 'local':
                        local_urls.append(result[1:])
        
        self.info.append(f"✓ GitHub URLs: {github_urls}")
        
        if local_urls:
            self.errors.append(f"✗ Local file paths found: {len(local_urls)}")
            for name, url in local_urls[:5]:
                self.errors.append(f"  - {name}: {url[:60]}...")
    
    def test_organic_terrain(self):
        """Test 7: Check for organic terrain boundaries (informational)"""
        print(f"\n{Color.BOLD}Test 7: Organic Terrain Boundaries{Color.END}")
        
        area_terrain_types = [
            'bua', 'wood', 'marsh', 'hill', 'ploughed', 'rocky', 'enclosure'
        ]
        
        area_terrain_count = 0
        
        for obj in self.save_data['ObjectStates']:
            if obj.get('Name') == 'Bag':
                for contained in obj.get('ContainedObjects', []):
                    nickname = contained.get('Nickname', '').lower()
                    if any(t in nickname for t in area_terrain_types):
                        area_terrain_count += 1
        
        self.info.append(f"✓ Area terrain pieces: {area_terrain_count}")
        
        if area_terrain_count >= 24:
            self.info.append(f"✓ All 24 area terrain pieces present (should have organic polygons)")
        else:
            self.warnings.append(f"⚠ Expected 24 area terrain pieces, found {area_terrain_count}")
    
    def run_all_tests(self) -> bool:
        """Run all tests and return overall pass/fail"""
        print(f"\n{Color.BOLD}{'='*70}{Color.END}")
        print(f"{Color.BOLD}DBR TTS SAVE FILE TEST FRAMEWORK{Color.END}")
        print(f"{Color.BOLD}{'='*70}{Color.END}")
        print(f"Save File: {os.path.basename(self.save_file_path)}")
        print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.load_save_file():
            return False
        
        # Run all tests
        self.test_save_metadata()
        self.test_table_configuration()
        self.test_asset_placement()
        self.test_unit_scaling()
        self.test_terrain_scaling()
        self.test_github_urls()
        self.test_organic_terrain()
        
        # Print results
        self._print_results()
        
        return len(self.errors) == 0
    
    def _print_results(self):
        """Print test results summary"""
        print(f"\n{Color.BOLD}{'='*70}{Color.END}")
        print(f"{Color.BOLD}TEST RESULTS{Color.END}")
        print(f"{Color.BOLD}{'='*70}{Color.END}")
        
        # Print errors
        if self.errors:
            print(f"\n{Color.RED}{Color.BOLD}ERRORS ({len(self.errors)}):{Color.END}")
            for error in self.errors:
                print(f"{Color.RED}{error}{Color.END}")
        
        # Print warnings
        if self.warnings:
            print(f"\n{Color.YELLOW}{Color.BOLD}WARNINGS ({len(self.warnings)}):{Color.END}")
            for warning in self.warnings:
                print(f"{Color.YELLOW}{warning}{Color.END}")
        
        # Print info
        if self.info:
            print(f"\n{Color.GREEN}{Color.BOLD}INFO ({len(self.info)}):{Color.END}")
            for info in self.info:
                print(f"{Color.GREEN}{info}{Color.END}")
        
        # Overall result
        print(f"\n{Color.BOLD}{'='*70}{Color.END}")
        if len(self.errors) == 0:
            print(f"{Color.GREEN}{Color.BOLD}✓ ALL TESTS PASSED{Color.END}")
            if self.warnings:
                print(f"{Color.YELLOW}  ({len(self.warnings)} warnings){Color.END}")
            print(f"{Color.BOLD}{'='*70}{Color.END}\n")
            return True
        else:
            print(f"{Color.RED}{Color.BOLD}✗ TESTS FAILED{Color.END}")
            print(f"{Color.RED}  {len(self.errors)} errors, {len(self.warnings)} warnings{Color.END}")
            print(f"{Color.BOLD}{'='*70}{Color.END}\n")
            return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python test_framework.py <save_file_path>")
        print("\nExample:")
        print("  python test_framework.py ~/Library/Tabletop\\ Simulator/Saves/DBR_*.json")
        sys.exit(1)
    
    save_file = sys.argv[1]
    
    framework = TTSTestFramework(save_file)
    success = framework.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
