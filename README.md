# Convert Planar Surfaces to Hatch in Rhino3D

This Rhino script allows you to convert **planar surfaces or polysurfaces** into solid hatch objects. It works by extracting the outer boundary of each face and generating a filled hatch based on that contour.

> **This tool acts as a utility to extract hatch regions from geometry — similar to duplicating a surface border and manually adding a hatch, but fully automated and with layer control.**

## What Does the Script Do?

The **Surfaces to Hatch** tool allows you to:

* Select multiple planar **surfaces or polysurfaces**.
* Validate that each has **only one face** and is **planar**.
* Extract the **outer border** of each valid face.
* Generate a solid hatch using the `"Solid"` hatch pattern.
* Automatically assign the hatch to either:

  * The original surface’s layer, or
  * The current active layer.
* Optionally delete the original surface after hatch creation.

Surfaces that fail the validation or hatch creation are selected and reported at the end.

## Why Use It?

This tool is useful when:

* You need to convert filled geometry into 2D representation for annotation or export.
* Generating **section drawings**, **plan views**, or **documentation**.
* Automating the repetitive process of duplicating borders and manually applying hatches.
* Creating clean vector hatch patterns from Rhino modelled forms.

## How to Use the Script

### Load the Script in Rhino

**Method 1**:

1. Type `_RunPythonScript` in the command line.
2. Browse to the location where you saved the script and select it.

### Method 2 Creating a Button or Alias for Easy Access (Optional)

#### Creating a Toolbar Button

1. **Right-click** on an empty area of the toolbar and select **New Button**.
2. In the **Button Editor**:

   * **Left Button Command**:

     ```plaintext
     ! _-RunPythonScript "FullPathToYourScript\surfaces_to_hatch.py"
     ```

     Replace `FullPathToYourScript` with the actual file path where the script is saved.
   * **Tooltip and Help**: e.g., `Convert planar surfaces to solid hatch regions`.
   * **Icon (Optional)**: You can assign an icon for easier access.

#### Creating an Alias

1. Go to **Tools > Options** and select the **Aliases** tab.

2. **Create a New Alias**:

   * **Alias**: e.g., `surf2hatch`
   * **Command Macro**:

     ```plaintext
     _-RunPythonScript "FullPathToYourScript\surfaces_to_hatch.py"
     ```

3. **Use the Alias**: Type the alias (e.g., `surf2hatch`) into the command line and press **Enter** to run the script.

### Using the Command

1. **Select** the surfaces or polysurfaces to convert.
2. When prompted:

   * Choose whether to **keep the original surface** after hatch creation.
   * Choose whether to assign the hatch to the **original object's layer** or the **current active layer**.
3. The script will:

   * Validate each object is a single-face, planar Brep.
   * Extract the outer boundary of each face.
   * Create solid hatches from those outlines.
   * Delete the original surface if chosen.
4. A message box will indicate:

   * Whether the conversion was successful.
   * Which objects (if any) failed and have been selected for review.

## Technical Notes

* Only **planar single-face surfaces** are supported.
* **Multi-face polysurfaces** or **non-planar geometry** are skipped.
* Hatch is created using the `"Solid"` hatch pattern.
* Border curves are deleted after use.
* Boundary extraction uses `rs.DuplicateSurfaceBorder(..., type=1)`, ensuring only outer loops are used.
* Hatch scale is fixed at `1.0`, and rotation is `0.0`.
