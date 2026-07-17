import os

def generate_marine_vault_system():
    # --- PARAMETRIC DIMENSIONS (in mm) ---
    wall_thick = 4.0        # Thick walls for structural CF-PETG integrity
    inner_height = 32.0     # Clear depth for horizontal SBC stacks
    
    # Chamber lengths (internal dimensions along X axis)
    ch_a_len = 25.4         # 1 inch slot for PB2-I #1
    ch_b_len = 25.4         # 1 inch slot for PB2-I #2
    ch_c_len = 25.4         # 1 inch slot for PB2-I #3
    ch_d_len = 65.0         # Expanded space for BeagleBone Blue
    
    inner_width = 110.0     # Wide enough to clear the BB-Blue layout
    
    # Gasket Profile (2mm silicone sponge cord)
    groove_w = 2.4          # 2.4mm track width provides perfect seating for 2mm cord
    groove_d = 3.0          # 3mm deep track
    knife_w = 1.6           # 1.6mm wide lid tooth (gives 0.4mm clearance on each side)
    knife_h = 2.4           # 2.4mm plunge depth into the track for strong compression
    
    # Aluminum Cooling Plate Step
    plate_thick = 3.0       # 3mm raw aluminum spine
    lip_width = 2.5         # 2.5mm shelf width to apply 3M Marine 5200 adhesive bead
    
    # Computed layout math
    ch_lengths = [ch_a_len, ch_b_len, ch_c_len, ch_d_len]
    total_inner_length = sum(ch_lengths) + (len(ch_lengths) - 1) * wall_thick
    outer_length = total_inner_length + (2 * wall_thick)
    outer_width = inner_width + (2 * wall_thick)
    outer_height = inner_height + wall_thick

    # =========================================================================
    # 1. GENERATE BASE SCAD FILE
    # =========================================================================
    base_scad = f"""// Auto-generated Marine Vault BASE
$fn = 40; 

module marine_vault_base() {{
    difference() {{
        // Main outer envelope
        cube([{outer_length}, {outer_width}, {outer_height}]);
        
        // Internal Chamber Cutouts
        {generate_chamber_cutouts(ch_lengths, wall_thick, inner_width, outer_height)}
        
        // Aluminum Cooling Plate Inset (Cut out from the absolute bottom)
        translate([{wall_thick - lip_width}, {wall_thick - lip_width}, -0.5]) 
            cube([{total_inner_length + (2 * lip_width)}, {inner_width + (2 * lip_width)}, {plate_thick + 0.5}]);
            
        // Gasket Track System (Top Face)
        {generate_gasket_grooves(ch_lengths, wall_thick, inner_width, outer_height, groove_w, groove_d)}
        
        // Stern Cable Glands (Chambers A,B,C: 2xM12 vertical, Chamber D: M16+M12)
        {generate_cable_glands(ch_lengths, wall_thick, inner_width, inner_height)}
        
        // Threaded Heat-Set Insert Pilot Holes
        {generate_base_fastener_holes(ch_lengths, wall_thick, inner_width, outer_height)}
    }}
}}
marine_vault_base();
"""

    # =========================================================================
    # 2. GENERATE LID SCAD FILE
    # =========================================================================
    lid_scad = f"""// Auto-generated Marine Vault LID
$fn = 40;

module marine_vault_lid() {{
    difference() {{
        // Main Cap Volume
        cube([{outer_length}, {outer_width}, {wall_thick}]);
        
        // Clearance Bolt Holes passing entirely through lid
        {generate_lid_screw_holes(ch_lengths, wall_thick, inner_width)}
    }}
    
    // Inverted Knife-Edge Gasket Press Rails
    translate([0, 0, {wall_thick}]) {{
        {generate_lid_knife_edges(ch_lengths, wall_thick, inner_width, groove_w, knife_w, knife_h)}
    }}
}}
marine_vault_lid();
"""

    with open("marine_vault_base.scad", "w") as f:
        f.write(base_scad)
    with open("marine_vault_lid.scad", "w") as f:
        f.write(lid_scad)
        
    print("Success: Generated 'marine_vault_base.scad' and 'marine_vault_lid.scad'")

# --- Helper Functions for Complex CSG Math Geometry ---

def generate_chamber_cutouts(lengths, wall, width, total_h):
    code = ""
    current_x = wall
    for length in lengths:
        # Cuts from just above the aluminum plate ceiling all the way to the top open deck
        code += f"        translate([{current_x}, {wall}, 3.0]) cube([{length}, {width}, {total_h}]);\n"
        current_x += length + wall
    return code

def generate_gasket_grooves(lengths, wall, width, out_height, g_w, g_d):
    code = "        // Perimeter Gasket Track\n"
    g_offset = (wall / 2) - (g_w / 2)
    # Outer continuous loop
    code += f"        translate([{g_offset}, {g_offset}, {out_height} - {g_d}]) difference() {{\n"
    code += f"            cube([{sum(lengths) + wall * len(lengths) + wall - 2*g_offset}, {width + 2*wall - 2*g_offset}, {g_d} + 1]);\n"
    code += f"            translate([{g_w}, {g_w}, -1]) cube([{sum(lengths) + wall * len(lengths) + wall - 2*g_offset - 2*g_w}, {width + 2*wall - 2*g_offset - 2*g_w}, {g_d} + 3]);\n"
    code += f"        }}\n"
    
    # Bulkhead cross sections
    current_x = wall
    for length in lengths[:-1]:
        current_x += length
        code += f"        translate([{current_x + wall/2 - g_w/2}, {wall}, {out_height} - {g_d}]) cube([{g_w}, {width}, {g_d} + 1]);\n"
        current_x += wall
    return code

def generate_lid_knife_edges(lengths, wall, width, g_w, k_w, k_h):
    # Centering math to drop exactly down middle of the base tracks
    track_center_offset = wall / 2
    edge_start = track_center_offset - (k_w / 2)
    
    code = "        // Outer Ring Knife Edge\n"
    code += f"        difference() {{\n"
    code += f"            translate([{edge_start}, {edge_start}, 0]) cube([{sum(lengths) + wall * len(lengths) + wall - 2*edge_start}, {width + 2*wall - 2*edge_start}, {k_h}]);\n"
    code += f"            translate([{edge_start + k_w}, {edge_start + k_w}, -1]) cube([{sum(lengths) + wall * len(lengths) + wall - 2*edge_start - 2*k_w}, {width + 2*wall - 2*edge_start - 2*k_w}, {k_h} + 2]);\n"
    code += f"        }}\n"
    
    code += "        // Internal Bulkhead Cross Knife Edges\n"
    current_x = wall
    for length in lengths[:-1]:
        current_x += length
        code += f"        translate([{current_x + wall/2 - k_w/2}, {wall}, 0]) cube([{k_w}, {width}, {k_h}]);\n"
        current_x += wall
    return code

def generate_cable_glands(lengths, wall, width, height):
    code = ""
    current_x = wall
    for i, length in enumerate(lengths):
        center_x = current_x + (length / 2)
        if i < 3: # Chambers A, B, C: Vertically stacked M12 lines
            m12_r = 6.1 # 12.2mm diameter clearance for M12 threads
            code += f"        translate([{center_x}, -1, {height * 0.35}]) rotate([-90, 0, 0]) cylinder(r={m12_r}, h={wall + 2});\n"
            code += f"        translate([{center_x}, -1, {height * 0.75}]) rotate([-90, 0, 0]) cylinder(r={m12_r}, h={wall + 2});\n"
        else: # Chamber D: Expanded horizontal row for M16 + M12
            m16_r = 8.1 # 16.2mm diameter clearance for M16 trunk
            m12_r = 6.1
            code += f"        translate([{current_x + (length * 0.3)}, -1, {height * 0.55}]) rotate([-90, 0, 0]) cylinder(r={m16_r}, h={wall + 2});\n"
            code += f"        translate([{current_x + (length * 0.7)}, -1, {height * 0.55}]) rotate([-90, 0, 0]) cylinder(r={m12_r}, h={wall + 2});\n"
        current_x += length + wall
    return code

def generate_base_fastener_holes(lengths, wall, width, out_height):
    code = ""
    hole_r = 2.1 # 4.2mm diameter for standard M3 brass heat-set inserts (short variant, 4mm deep)
    hole_d = 4.5
    z_pos = out_height - hole_d
    
    current_x = wall / 2
    for length in lengths:
        code += f"        translate([{current_x}, {wall / 2}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
        code += f"        translate([{current_x}, {width + wall * 1.5}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
        current_x += length + wall
    code += f"        translate([{current_x - wall/2}, {wall / 2}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
    code += f"        translate([{current_x - wall/2}, {width + wall * 1.5}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
    return code

def generate_lid_screw_holes(lengths, wall, width):
    code = ""
    bolt_r = 1.7 # 3.4mm diameter clearance for an M3 cap screw thread to slip through
    
    current_x = wall / 2
    for length in lengths:
        code += f"        translate([{current_x}, {wall / 2}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
        code += f"        translate([{current_x}, {width + wall * 1.5}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
        current_x += length + wall
    code += f"        translate([{current_x - wall/2}, {wall / 2}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
    code += f"        translate([{current_x - wall/2}, {width + wall * 1.5}, -1]) cylinder(r={bolt_r}, h={wall + 2});\n"
    return code

if __name__ == "__main__":
    generate_marine_vault_system()
    
# =========================================================================
# ATTRIBUTION & PROVENANCE
# Generated by: Gemini 3.5 Flash (Adaptive AI Collaborator)
# Date: July 17, 2026
# Project: Parametric IP67 Marine Compute Vault Engine
# Target Material: Carbon Fiber PETG (CF-PETG) FDM Print
# =========================================================================