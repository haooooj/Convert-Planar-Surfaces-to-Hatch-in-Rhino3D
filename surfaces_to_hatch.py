import rhinoscriptsyntax as rs
import Rhino

def is_brep_planar(obj_id, tolerance=1e-6):
    """
    Returns True if the object's Brep is planar, False otherwise.
    For a single-face surface, we check that face's IsPlanar(tolerance).
    For a polysurface, we can either skip or require all faces be planar 
    and coplanar. Currently, we just skip if more than one face.
    """
    brep = rs.coercebrep(obj_id)
    if not brep:
        return False

    face_count = brep.Faces.Count
    if face_count < 1:
        return False

    # If only handling single-face surfaces, skip if more than one face
    if face_count > 1:
        return False

    face = brep.Faces[0]
    return face.IsPlanar(tolerance)

def surfaces_to_hatch():
    # Prompt user to select planar surfaces/polysurfaces
    obj_ids = rs.GetObjects(
        "Select planar surfaces to convert to hatch",
        preselect=True,
        filter=8+16  # surfaces + polysurfaces
    )
    if not obj_ids:
        print("No surfaces selected.")
        return

    hatch_pattern = "Solid"  # Must exist in Rhino

    # Ask whether to keep the original surfaces after conversion
    keep_str = rs.GetString(
        "Keep original surfaces? (Yes/No)",
        "Yes",
        ["Yes", "No"]
    )
    if not keep_str:
        print("Cancelled keep-surface prompt.")
        return
    keep_surfaces = (keep_str.lower() == "yes")
    
    # Ask user whether to place the hatch on the original surface's layer or the current active layer
    layer_choice = rs.GetString(
        "Place hatch on the original surface's layer or the current layer? (Original/Current)",
        "Original",
        ["Original", "Current"]
    )
    if not layer_choice:
        print("Cancelled hatch layer choice prompt.")
        return

    # List to track surfaces that failed to convert
    failed_objs = []

    for obj_id in obj_ids:
        hatch_created_count = 0
        if is_brep_planar(obj_id):
            # Duplicate the outer border
            border_curves = rs.DuplicateSurfaceBorder(obj_id, type=1)  # 1 = outer border
            if border_curves:
                # Create hatches from these curves
                for c_id in border_curves:
                    new_hatch_id = rs.AddHatch(c_id, hatch_pattern, 1.0, 0.0)
                    if not new_hatch_id:
                        print("Failed to create hatch for border curve {}".format(c_id))
                    else:
                        hatch_created_count += 1
                        # If user chose 'Original', assign the hatch to the original surface's layer
                        if layer_choice.lower() == "original":
                            original_layer = rs.ObjectLayer(obj_id)
                            rs.ObjectLayer(new_hatch_id, original_layer)
                # Delete the border curves
                rs.DeleteObjects(border_curves)
            else:
                print("Could not obtain an outer border from object {}".format(obj_id))
            
            # If no hatch was created, consider it a failed conversion
            if hatch_created_count == 0:
                failed_objs.append(obj_id)
            else:
                # If user chose not to keep the original surface, delete it
                if not keep_surfaces:
                    rs.DeleteObject(obj_id)
        else:
            print("Skipping non-planar or multi-face object {}".format(obj_id))
            failed_objs.append(obj_id)
    
    # If any surfaces failed to convert, select them and display a message box
    if failed_objs:
        rs.SelectObjects(failed_objs)
        failed_msg = "The following surfaces could not be converted to hatch:\n" + ", ".join(failed_objs)
        rs.MessageBox(failed_msg, 0, "Conversion Failed")
    else:
        rs.MessageBox("All surfaces were successfully converted to hatch.", 0, "Conversion Successful")

def main():
    surfaces_to_hatch()

if __name__ == "__main__":
    main()
