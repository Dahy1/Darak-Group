/*
* v2.6.0
* Unlimited Scroll Text Animation - Unlimited Elements for Elementor.
* © Unlimited Elements for Elementor, Adarsh Pawar.
* Libraries : GSAP, GSAP ScrollTrigger, GSAP SplitText, Lenis (Smooth Scrolling).
*/

function UE_ScrollTextAnimation(objWidget) {

    if (!objWidget.length) return;

    var objWidgetText = objWidget.find('.ue-reveal-text');
    var activeColor = objWidget.attr('data-active-color');
    var inactiveColor = objWidget.attr('data-inactive-color');
    var activeRotate = parseInt(objWidget.attr('data-active-rotate'), 10) || 0;
    var inactiveRotate = parseInt(objWidget.attr('data-inactive-rotate'), 10) || 0;
    var activeScale = parseInt(objWidget.attr('data-active-scale'), 10) || 100;
    var inactiveScale = parseInt(objWidget.attr('data-inactive-scale'), 10) || 100;
    var activeBlur = parseInt(objWidget.attr('data-active-blur'), 10) || 0;
    var inactiveBlur = parseInt(objWidget.attr('data-inactive-blur'), 10) || 0;
    var activeOpacity = parseInt(objWidget.attr('data-active-opacity'), 10) || 100;
    var inactiveOpacity = parseInt(objWidget.attr('data-inactive-opacity'), 10) || 100;
    var revealType = objWidget.attr('data-reveal-type') || 'chars';
    var revealFrom = objWidget.attr('data-reveal-from') || "start";
    var revealSpeed = parseInt(objWidget.attr('data-reveal-speed'), 10) || 50;
    var revealSmoothness = parseInt(objWidget.attr('data-reveal-smoothness'), 10) || 4;
    var revealRepeat = parseInt(objWidget.attr('data-repeat-reveal'), 10) || 0;
    var animationEasing = objWidget.attr('data-animation-easing') || 'none';
    var showMarkers = objWidget.attr('data-markers') === 'true';
    var animationStartPOS = parseInt(objWidget.attr('data-animation-start'), 10) || 40;
    var animationEndPOS = parseInt(objWidget.attr('data-animation-end'), 10) || 30;
    var pinWidget = objWidget.attr('data-pin') === 'true';
    var enablesSmoothScroll = objWidget.attr('data-smooth-scroll') === 'true';
    var scrollDuration = objWidget.attr('data-pin') === 'true';
    var pinWidget = objWidget.attr('data-pin') === 'true';
    var posYActive = parseInt(objWidget.attr('data-posY-active'), 10) || 0;
    var posY = parseInt(objWidget.attr('data-posY'), 10) || 0;
    var rorateXActive = parseInt(objWidget.attr('data-rotateX-active'), 10) || 0;
    var rotateX = parseInt(objWidget.attr('data-rotateX-inactive'), 10) || 0;
    var rorateYActive = parseInt(objWidget.attr('data-rotateY-active'), 10) || 0;
    var rotateY = parseInt(objWidget.attr('data-rotateY-inactive'), 10) || 0;

    /* --- Using smooth scroll widget instead ---
    if (!window.__ueLenis) {
        window.__ueLenis = new Lenis({
            smooth: true,
            multiplier: 1,
            // wheelMultiplier: 1,
            // touchMultiplier: 1.5,
            // infinite: true,
            easing: (t) => t * (2 - t),
            smoothTouch: true,
            lerp: 0.05,
            duration: 1.2
        }); 
        gsap.ticker.add((time) => {
            window.__ueLenis.raf(time * 1000);
        });
        gsap.ticker.lagSmoothing(0);
    }
    */

    /* GSAP */

    if (!window.__ueGsapInit) {
        gsap.registerPlugin(ScrollTrigger, SplitText);
        
  const ua = navigator.userAgent || "";
  const isIOS = /iP(ad|hone|od)/.test(ua);
  const isChromeIOS = /CriOS/.test(ua);
  if (!(isIOS && isChromeIOS)) {
    ScrollTrigger.normalizeScroll(true);
  }


        window.__ueGsapInit = true;
    }

    function initAnimation() {

        /* ANIMATION */

        var splitType;
        switch (revealType) {
            case 'chars':
                splitType = 'words, chars';
                break;
            case 'lines':
                splitType = 'lines';
                break;
            case 'words':
            default:
                splitType = 'words';
        }

        const ueText = new SplitText(objWidgetText[0], {
            type: splitType
        });

        var targets;

        if (revealType === 'chars') {
            targets = ueText.chars;
        } else if (revealType === 'lines') {
            targets = ueText.lines;
        } else {
            targets = ueText.words;
        }

        /* SCROLLTRIGGER CONFIG */

        var scrollTriggerConfig = {
            trigger: objWidgetText[0],
            start: `top bottom-=${animationStartPOS}%`,
            end: `bottom bottom-=${animationEndPOS}%`,
            scrub: revealSmoothness,
            pin: pinWidget,
            ease: animationEasing,
            markers: showMarkers,
            onEnter: () => objWidget.addClass('ue-animating'),
            onEnterBack: () => objWidget.addClass('ue-animating'),
            onLeave: () => objWidget.removeClass('ue-animating'),
            onLeaveBack: () => objWidget.removeClass('ue-animating')
        };

        //  CLEANUP (for Elementor editor)
        ScrollTrigger.getAll().forEach((st) => {
            if (st.trigger === objWidgetText[0]) {
                st.kill(true);
            }
        });

        gsap.killTweensOf(objWidgetText.find('*'));

        document.querySelectorAll(
            '.gsap-marker-start, .gsap-marker-end, .gsap-marker-scroller-start, .gsap-marker-scroller-end'
        ).forEach(el => el.remove());

        ScrollTrigger.refresh(true);

        // ----------------------

        gsap.fromTo(
            targets,
            {
                color: inactiveColor,
                rotate: inactiveRotate,
                scale: inactiveScale / 100,
                opacity: inactiveOpacity / 100,
                filter: `blur(${inactiveBlur}px)`,
                y: posY,
                rotationX:rotateX,
                rotationY:rotateY,
            },
            {
                color: activeColor,
                rotate: activeRotate,
                scale: activeScale / 100,
                opacity: activeOpacity / 100,
                filter: `blur(${activeBlur}px)`,
                y: posYActive,
                rotationX:rorateXActive,
                rotationY:rorateYActive,
                stagger: {
                    each: revealSpeed / 1000,
                    repeat: revealRepeat,
                    from: revealFrom,
                    // ease: 'power2.inOut',
                },
                scrollTrigger: scrollTriggerConfig
            }
        );
        /*
        if (revealType === 'lines') {
          ScrollTrigger.addEventListener('refresh', function () {
            ueText.split();
          });
        }
        */
        objWidget.addClass('uc-inited');
    }

    // Initialize
    if (objWidget.hasClass('uc-inited') == false) {
      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(() => {
            initAnimation();
            ScrollTrigger.refresh(true);
        });
      } else {
        // Fallback for old browsers
        setTimeout(() => {
            initAnimation();
            ScrollTrigger.refresh(true);
        }, 300);
      }
    }
}