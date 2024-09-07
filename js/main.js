
function main() {

(function () {
   'use strict';
   
  	$('a.page-scroll').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
          if (target.length) {
            $('html,body').animate({
              scrollTop: target.offset().top - 40
            }, 900);
            return false;
          }
        }
      });

    //upload
    var dropzone = new Dropzone('#demo-upload', {
      previewTemplate: document.querySelector('#preview-template').innerHTML,
      parallelUploads: 2,
      thumbnailHeight: 120,
      thumbnailWidth: 120,
      maxFilesize: 400,
      filesizeBase: 1000,
      thumbnail: function(file, dataUrl) {
        if (file.previewElement) {
          file.previewElement.classList.remove("dz-file-preview");
          var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
          for (var i = 0; i < images.length; i++) {
            var thumbnailElement = images[i];
            thumbnailElement.alt = file.name;
            thumbnailElement.src = dataUrl;
          }
          setTimeout(function() { file.previewElement.classList.add("dz-image-preview"); }, 1);
        }
      }
    
    });
    
    
    // Now fake the file upload, since GitHub does not handle file uploads
    // and returns a 404
    
    var minSteps = 6,
        maxSteps = 60,
        timeBetweenSteps = 100,
        bytesPerStep = 100000;
    
    dropzone.uploadFiles = function(files) {
      var self = this;
    
      for (var i = 0; i < files.length; i++) {
    
        var file = files[i];
        totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));
    
        for (var step = 0; step < totalSteps; step++) {
          var duration = timeBetweenSteps * (step + 1);
          setTimeout(function(file, totalSteps, step) {
            return function() {
              file.upload = {
                progress: 100 * (step + 1) / totalSteps,
                total: file.size,
                bytesSent: (step + 1) * file.size / totalSteps
              };
    
              self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
              if (file.upload.progress == 100) {
                file.status = Dropzone.SUCCESS;
                self.emit("success", file, 'success', null);
                self.emit("complete", file);
                self.processQueue();
                //document.getElementsByClassName("dz-success-mark").style.opacity = "1";
              }
            };
          }(file, totalSteps, step), duration);
        }
      }
    }

	
    // Show Menu on Book
    $(window).bind('scroll', function() {
        var navHeight = $(window).height() - 500;
        if ($(window).scrollTop() > navHeight) {
            $('.navbar-default').addClass('on');
        } else {
            $('.navbar-default').removeClass('on');
        }
    });

    $('body').scrollspy({ 
        target: '.navbar-default',
        offset: 80
    });

	// Hide nav on click
  $(".navbar-nav li a").click(function (event) {
    // check if window is small enough so dropdown is created
    var toggle = $(".navbar-toggle").is(":visible");
    if (toggle) {
      $(".navbar-collapse").collapse('hide');
    }
  });
	
  	// Portfolio isotope filter
    $(window).load(function() {
        var $container = $('.portfolio-items');
        $container.isotope({
            filter: '*',
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: false
            }
        });
        $('.cat a').click(function() {
            $('.cat .active').removeClass('active');
            $(this).addClass('active');
            var selector = $(this).attr('data-filter');
            $container.isotope({
                filter: selector,
                animationOptions: {
                    duration: 750,
                    easing: 'linear',
                    queue: false
                }
            });
            return false;
        });

    });
	
    // Nivo Lightbox 
    $('.portfolio-item a').nivoLightbox({
            effect: 'slideDown',  
            keyboardNav: true,                            
        });

}());


}
main();
