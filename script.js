$(document).ready(function(){
    $("#chat").on("input", function() {
        this.style.height = "auto"; // Reset height to auto before calculating new height
        this.style.height = (this.scrollHeight) + "px"; // Set new height based on content

        // Expand the parent `.chat-box`
        $(".chat-box").css("min-height", this.scrollHeight + 20 + "px");
    });

    $(".submit-button").click(function(){
        $(".chat-form").submit();
    });
});
