// Auto-generated Marine Vault OpenSCAD File
$fn = 40; // Circle resolution

// Main Compilation Module
module marine_vault_base() {
    difference() {
        // 1. Solid Outer Block
        cube([161.2, 118.0, 36.0]);
        
        // 2. Clear out the Open Bottom Windows for each chamber
                translate([4.0, 4.0, -1]) cube([25.4, 110.0, 32.0 + 1]);
        translate([33.4, 4.0, -1]) cube([25.4, 110.0, 32.0 + 1]);
        translate([62.8, 4.0, -1]) cube([25.4, 110.0, 32.0 + 1]);
        translate([92.19999999999999, 4.0, -1]) cube([65.0, 110.0, 32.0 + 1]);

        
        // 3. Cut out the Top Interstitial Knife-Edge/Gasket Track
                // Perimeter Gasket Track
        translate([0.8999999999999999, 0.8999999999999999, 36.0 - 3.0]) difference() {
            cube([159.39999999999998, 116.2, 3.0 + 1]);
            translate([2.2, 2.2, -1]) cube([154.99999999999997, 111.8, 3.0 + 3]);
        }
        // Internal Bulkhead Gasket Cross-tracks
        translate([30.299999999999997, 4.0, 36.0 - 3.0]) cube([2.2, 110.0, 3.0 + 1]);
        translate([59.699999999999996, 4.0, 36.0 - 3.0]) cube([2.2, 110.0, 3.0 + 1]);
        translate([89.1, 4.0, 36.0 - 3.0]) cube([2.2, 110.0, 3.0 + 1]);

        
        // 4. Punch out the Stern Cable Glands (Chambers A,B,C: 2xM12 vertical, Chamber D: M16+M12)
                // Gland Drilling Ports (facing stern along Y-axis wall)
        translate([16.7, -1, 9.6]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([16.7, -1, 22.4]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([46.099999999999994, -1, 9.6]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([46.099999999999994, -1, 22.4]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([75.5, -1, 9.6]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([75.5, -1, 22.4]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);
        translate([111.69999999999999, -1, 16.0]) rotate([-90, 0, 0]) cylinder(r=8.1, h=6.0);
        translate([137.7, -1, 16.0]) rotate([-90, 0, 0]) cylinder(r=6.1, h=6.0);

        
        // 5. Pilot holes for Fasteners (M3 Threaded Heat-Set Inserts)
                // M3 Heat-Set Insert Pilot Holes (4.2mm deep, 4.0mm diameter)
        translate([2.0, 2.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([2.0, 116.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([31.4, 2.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([31.4, 116.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([60.8, 2.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([60.8, 116.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([90.19999999999999, 2.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([90.19999999999999, 116.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([157.2, 2.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);
        translate([157.2, 116.0, 31.5]) cylinder(r=2.0, h=4.5 + 1);

    }
}

marine_vault_base();
