function fetch(url) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            alert(request.responseText);
        }
    }
    request.open("POST", url, true);
    request.send();
}



$(".DELETE").click(
    function(event){
        // Hide it
        // $(this).parent().parent().parent().hide();
        // Background request to ignore this job.
        var request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                alert(request.responseText);
            }
        }
        request.open("POST", "/api/job-status/ignore?jobid="+ String(this.id).replace("&", "Ampersand"), true);
        request.send();
    }
)

$(".IgnoreButton").click(
    function(event){
        // Hide from immediate view
        $(this).parent().parent().parent().hide();
        fetch("/api/job-status/ignore?jobid="+ String(this.id).replace("&", "Ampersand"));
        // Background request to ignore this job.
    }
);

$(".InterestedButton").click(
    function(event){
        // Background request to ignore this job.
        fetch("/api/job-status/interested?jobid="+ String(this.id).replace("&", "Ampersand"));
    }
);

$(".AppliedButton").click(
    function(event){
        // Background request to ignore this job.
        fetch("/api/job-status/applied?jobid="+ String(this.id).replace("&", "Ampersand"));
    }
)

$(".INTERVIEW").click(
    function(event){
        fetch("/api/job-status/interview?jobid="+ String(this.id).replace("&", "Ampersand"));
    }
)
$(".OFFER").click(
    function(event){
        fetch("/api/job-status/offer?jobid="+ String(this.id).replace("&", "Ampersand"));
    }
)
