var subjectObject = {
    "B.Tech": {
        "ECE": ["B.Tech. Electronics and Communication Engineering"],
        "EEE": ["B.Tech. Electrical and Electronics Engineering"],
        "IT": ["B.Tech. Information Technology","B.Tech. Computer Science and Engineering"],
        "CIVIL": ["B.Tech. CIVIL"],
    },
    "PG": {
        "MCA": ["MCA - Master of Computer Applications"]
    }
}
window.onload = function () {
    var programSel = document.getElementById("prog");
    var departmentSel = document.getElementById("dept");
    var courseSel = document.getElementById("course");
    for (var x in subjectObject) {
        programSel.options[programSel.options.length] = new Option(x, x);
    }
    programSel.onchange = function () {
        //empty Chapters- and Topics- dropdowns
        courseSel.length = 1;
        departmentSel.length = 1;
        //display correct values
        for (var y in subjectObject[this.value]) {
            departmentSel.options[departmentSel.options.length] = new Option(y, y);
        }
    }
    departmentSel.onchange = function () {
        //empty Chapters dropdown
        courseSel.length = 1;
        //display correct values
        var z = subjectObject[programSel.value][this.value];
        for (var i = 0; i < z.length; i++) {
            courseSel.options[courseSel.options.length] = new Option(z[i], z[i]);
        }
    }
}
