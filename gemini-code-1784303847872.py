import os

def generate_marine_vault_scad(filename="marine_vault.scad"):
    # --- PARAMETRIC DIMENSIONS (in mm) ---
    wall_thick = 4.0        # Robust walls for CF-PETG structural integrity
    inner_height = 32.0     # Clear depth for horizontal SBC stacks
    
    # Chamber lengths (internal dimensions along X axis)
    ch_a_len = 25.4         # 1 inch slot for PB2-I #1
    ch_b_len = 25.4         # 1 inch slot for PB2-I #2
    ch_c_len = 25.4         # 1 inch slot for PB2-I #3
    ch_d_len = 65.0         # Expanded space for BeagleBone Blue
    
    inner_width = 110.0     # Wide enough to clear the BB-Blue layout
    
    # Gasket Profile
    groove_w = 2.2          # Fit for 2mm silicone sponge cord
    groove_d = 3.0          # Depth of compression channel
    
    # Computed layout math
    ch_lengths = [ch_a_len, ch_b_len, ch_c_len, ch_d_len]
    total_inner_length = sum(ch_lengths) + (len(ch_lengths) - 1) * wall_thick
    outer_length = total_inner_length + (2 * wall_thick)
    outer_width = inner_width + (2 * wall_thick)
    outer_height = inner_height + wall_thick # Open bottom layout

    scad_code = f"""// Auto-generated Marine Vault OpenSCAD File
$fn = 40; // Circle resolution

// Main Compilation Module
module marine_vault_base() {{
    difference() {{
        // 1. Solid Outer Block
        cube([{outer_length}, {outer_width}, {outer_height}]);
        
        // 2. Clear out the Open Bottom Windows for each chamber
        {generate_chamber_cutouts(ch_lengths, wall_thick, inner_width, inner_height)}
        
        // 3. Cut out the Top Interstitial Knife-Edge/Gasket Track
        {generate_gasket_grooves(ch_lengths, wall_thick, inner_width, outer_height, groove_w, groove_d)}
        
        // 4. Punch out the Stern Cable Glands (Chambers A,B,C: 2xM12 vertical, Chamber D: M16+M12)
        {generate_cable_glands(ch_lengths, wall_thick, inner_width, inner_height)}
        
        // 5. Pilot holes for Fasteners (M3 Threaded Heat-Set Inserts)
        {generate_fastener_holes(ch_lengths, wall_thick, inner_width, outer_height)}
    }}
}}

marine_vault_base();
"""
    with open(filename, "w") as f:
        f.write(scad_code)
    print(f"Success: OpenSCAD model generated and saved to {filename}")

def generate_chamber_cutouts(lengths, wall, width, height):
    code = ""
    current_x = wall
    for i, length in enumerate(lengths):
        # Cuts right through the bottom (z=-1) up to the internal ceiling height
        code += f"        translate([{current_x}, {wall}, -1]) cube([{length}, {width}, {height} + 1]);\n"
        current_x += length + wall
    return code

def generate_gasket_grooves(lengths, wall, width, out_height, g_w, g_d):
    code = "        // Perimeter Gasket Track\n"
    # Offsets track to sit centered along the middle of the perimeter walls
    g_offset = wall / 2 - g_w / 2
    # Outer ring
    code += f"        translate([{g_offset}, {g_offset}, {out_height} - {g_d}]) difference() {{\n"
    code += f"            cube([{sum(lengths) + wall * len(lengths) + wall - 2*g_offset}, {width + 2*wall - 2*g_offset}, {g_d} + 1]);\n"
    code += f"            translate([{g_w}, {g_w}, -1]) cube([{sum(lengths) + wall * len(lengths) + wall - 2*g_offset - 2*g_w}, {width + 2*wall - 2*g_offset - 2*g_w}, {g_d} + 3]);\n"
    code += f"        }}\n"
    
    # Internal bulkhead tracks
    code += "        // Internal Bulkhead Gasket Cross-tracks\n"
    current_x = wall
    for length in lengths[:-1]:
        current_x += length
        # Center the channel over the internal partition wall
        code += f"        translate([{current_x + wall/2 - g_w/2}, {wall}, {out_height} - {g_d}]) cube([{g_w}, {width}, {g_d} + 1]);\n"
        current_x += wall
    return code

def generate_cable_glands(lengths, wall, width, height):
    code = "        // Gland Drilling Ports (facing stern along Y-axis wall)\n"
    current_x = wall
    for i, length in enumerate(lengths):
        center_x = current_x + (length / 2)
        if i < 3: # Chambers A, B, C: Vertically stacked M12 glands
            m12_drill_rad = 6.1 # 12.2mm diameter clearance for M12 threads
            # Lower Gland (Power/CAN)
            code += f"        translate([{center_x}, -1, {height * 0.3}]) rotate([-90, 0, 0]) cylinder(r={m12_drill_rad}, h={wall + 2});\n"
            # Upper Gland (OneNet Ethernet)
            code += f"        translate([{center_x}, -1, {height * 0.7}]) rotate([-90, 0, 0]) cylinder(r={m12_drill_rad}, h={wall + 2});\n"
        else: # Chamber D: Side-by-Side M16 and M12 Glands due to wider space
            m16_drill_rad = 8.1 # 16.2mm diameter clearance for M16 threads
            m12_drill_rad = 6.1
            code += f"        translate([{current_x + (length * 0.3)}, -1, {height * 0.5}]) rotate([-90, 0, 0]) cylinder(r={m16_drill_rad}, h={wall + 2});\n"
            code += f"        translate([{current_x + (length * 0.7)}, -1, {height * 0.5}]) rotate([-90, 0, 0]) cylinder(r={m12_drill_rad}, h={wall + 2});\n"
        current_x += length + wall
    return code

def generate_fastener_holes(lengths, wall, width, out_height):
    code = "        // M3 Heat-Set Insert Pilot Holes (4.2mm deep, 4.0mm diameter)\n"
    hole_r = 2.0
    hole_d = 4.5
    z_pos = out_height - hole_d
    
    # Places pilot points at every structural bulkhead intersection corner
    current_x = wall / 2
    for length in lengths:
        code += f"        translate([{current_x}, {wall / 2}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
        code += f"        translate([{current_x}, {width + wall * 1.5}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
        current_x += length + wall
    # Final corner set
    code += f"        translate([{current_x - wall/2}, {wall / 2}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
    code += f"        translate([{current_x - wall/2}, {width + wall * 1.5}, {z_pos}]) cylinder(r={hole_r}, h={hole_d} + 1);\n"
    return code

if __name__ == "__main__":
    generate_marine_vault_scad()
    
# =========================================================================
# ATTRIBUTION & PROVENANCE
# Generated by: Gemini 3.5 Flash (Adaptive AI Collaborator)
# Date: July 17, 2026
# Project: Parametric IP67 Marine Compute Vault Engine
# Target Material: Carbon Fiber PETG (CF-PETG) FDM Print
# =========================================================================