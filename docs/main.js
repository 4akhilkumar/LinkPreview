function escapeHTMLChar(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/!/g, '&excl;');
}

function link_preview(preview_url) {
    $.ajax({
        url: "https://rinjo.herokuapp.com/link_preview/",
        type: 'post',
        contentType: "application/json",
        data: JSON.stringify({
            url: preview_url
        }),
        success: function(data) {
            html_data = `
                <div class="link-preview">
                    <div class="link-preview-img">
                        <img src="data:image/png;base64,${data.image}" id="id_link-preview-img" alt="">
                    </div>
                    <div class="link-preview-title-description">
                        <div class="link-preview-title">
                            <h3 id="id_link-preview-title">
                                ${escapeHTMLChar(data.title)}
                            </h3>
                        </div>
                        <div class="link-preview-description">
                            <p id="id_link-preview-description">
                                ${escapeHTMLChar(data.description)}
                            </p>
                        </div>
                    </div>
                </div>
            `;
            // remove the child inside the div class="link-preview-container"
            $(".link-preview-container").empty();
            // append the html_data to the div class="link-preview-container"
            $(".link-preview-container").append(html_data);
        },
        error: function(data) {
            console.log(data);
        }
    });
}

// if user clicked on button id="id_btn-get-link-preview" then get the value of input id="id_url"
$("#id_btn-get-link-preview").click(function() {
    var url = $("#id_url").val();
    link_preview(url);
    loading_data = `
        <div class="showbox">
            <div class="loader">
                <svg class="circular" viewBox="25 25 50 50">
                <circle class="path" cx="50" cy="50" r="20" fill="none" stroke-width="2" stroke-miterlimit="10"/>
                </svg>
            </div>
        </div>
    `;

    $(".link-preview-container").empty();
    $(".link-preview-container").append(loading_data);
});