# DBR Wargaming Assets for Tabletop Simulator

Renaissance wargaming assets for **De Bellis Renationis (DBR)** rules in Tabletop Simulator.

## 📦 Contents

### AssetBundles (.unity3d files)
140+ game assets ready for Tabletop Simulator:

**Terrain Features:**
- **Hills** (6 variants):
  - Gentle hills with visible ridgelines (small, medium, large)
  - Steep hills with prominent ridgelines - area terrain (small, medium, large)
- **Water features** (5): Coastline, rivers, fords
- **Roads** (4): Straight, bend, crossroads, T-junction
- **Area terrain** (22+): BUAs, woods, marshes, rough/rocky ground, fields, enclosures

**Military Units:**
- **Cavalry** (10+): Lancers, demi-lancers, light horse, men-at-arms
- **Infantry** (30+): Pikemen, billmen, longbowmen, arquebusiers
- **Artillery & Train** (10+): Cannons, organ guns, wagons, baggage

**Game Tools:**
- Measure stick (40mm)
- Disorder markers
- Commander markers
- Dice bags

**Playing Surface:**
- Custom 6x4 foot grass table mesh

### TTS Save Files
Pre-configured Tabletop Simulator save files:
- `DBR_Grass_Table.json` - Full setup with grass table and all assets
- `DBR_Metallic_Lead_Flock.json` - Alternative setup

## 🎨 Materials

All assets feature automatic material detection:
- **Blue water** - Rivers, ponds, seas
- **Brown shores** - Banks, beaches
- **Dirt roads** - Paths, tracks
- **Green flock bases** - Unit bases
- **Original textures** - Buildings
- **Metallic lead** - Figures and terrain

## 🔗 Usage in TTS

### Access URLs
Assets are available at:
```
https://raw.githubusercontent.com/krumphau/DBR_assets/main/ASSET_NAME.unity3d
```

**Examples:**
```
https://raw.githubusercontent.com/krumphau/DBR_assets/main/gentle_hill_small.unity3d
https://raw.githubusercontent.com/krumphau/DBR_assets/main/english_billman_15mm_4up_40x20mm.unity3d
https://raw.githubusercontent.com/krumphau/DBR_assets/main/waterway_coastline_4x2ft.unity3d
```

### Loading in TTS

1. **Load a save file:**
   - Download a save file from `TTS_Saves/`
   - Place in `~/Documents/My Games/Tabletop Simulator/Saves/` (Windows)
   - Or `~/Library/Tabletop Simulator/Saves/` (Mac)
   - Load in TTS: Games → Saved Games

2. **Use individual assets:**
   - In TTS: Objects → Components → Custom → AssetBundle
   - Paste GitHub URL in AssetBundle URL field
   - Click import

## 📐 Scale

15mm wargaming scale (1:100)
- Base sizes: 40x20mm (infantry), 40x30mm (cavalry), 40x40mm (artillery/terrain)
- TTS scale: 0.015 for all assets

## 🎓 Features

### Hills with Visible Ridgelines
All hills now feature prominent ridgelines running along the center:
- **Gentle hills**: Soft, rounded ridges for cover and elevation (20-30° slopes)
- **Steep hills**: Sharp, dramatic ridges for area terrain (45-60° slopes)

### Area Terrain
Organic, non-rectangular bases for natural appearance:
- BUAs: 30-35% edge variation
- Woods: 40-50% edge variation  
- Marshes: 45-55% edge variation

### Waterway Features
Large terrain features (up to 4x2 feet) with:
- Blue flowing water surfaces
- Brown sandy shores
- Green bases

## 🛠️ Technical Details

**Created with:**
- Blender (3D modeling)
- Unity (AssetBundle creation)
- MCP (Model Context Protocol) integration

**Workflow:**
- Blender → OBJ/FBX export
- Unity → Material assignment + AssetBundle build
- GitHub → Public hosting
- TTS → Game deployment

## 📝 License

Assets created for personal and educational use in Tabletop Simulator.

## 🤝 Contributing

These assets were created for the DBR wargaming community. Feel free to use them in your own TTS games!

## 📧 Contact

**GitHub:** [krumphau](https://github.com/krumphau)  
**Repository:** [DBR_assets](https://github.com/krumphau/DBR_assets)

---

**Last Updated:** January 14, 2026  
**Total Assets:** 140+ AssetBundles  
**Total Size:** ~500MB

🎮 **Happy Wargaming!** ⚔️
