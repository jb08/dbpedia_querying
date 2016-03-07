//Modified Twitter Bootstrap JS from Template

$(function() {
	$("#queryForm input,#queryForm textarea").jqBootstrapValidation({
		preventSubmit: true,
		submitError: function($form, event, errors) {
		},
		submitSuccess: function($form, event) {

			alert("Success in valid");
            // Prevent spam click and default submit behaviour
            $("#btnSubmit").attr("disabled", true);
            event.preventDefault();
			//get user input
			var title = $("input#title").val();
			var author = $("input#author").val();
			alert(title);
			var bookTitle = title;

			$.ajax({
				url: "query_me.php",
				type: "POST",
				data: {
					title: title,
					author: author
				},
                dataType: "json",
				cache: false,
                success: function(data) {
                    // Enable button & show success message
                    $("#btnSubmit").attr("disabled", false);
                    $('#success').html("<div class='alert alert-success'>");
                    $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-success')
                        .append("<strong>Success! </strong>");
                    $('#success > .alert-success')
                        .append('</div>');
                },
                error: function(data) {
                    // Fail message
                    $('#success').html("<div class='alert alert-danger'>");
                    $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-danger').append("<strong>Sorry " + bookTitle + ", it seems that my mail server is not responding. Please try again later!");
                    $('#success > .alert-danger').append('</div>');
                },
			})
		},
		filter: function() {
            return $(this).is(":visible");
        },
	});

	$("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });
});

// When clicking on Full hide fail/success boxes
$('#name').focus(function() {
    $('#success').html('');
});

// When clicking on Full hide fail/success boxes
