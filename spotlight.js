/* A decorative cursor glow. No page features depend on this script. */
(() => {
    const spotlight = document.querySelector('.cursor-spotlight');
    if (!spotlight) return;

    const enabled = window.matchMedia(
        '(any-hover: hover) and (any-pointer: fine) and (prefers-reduced-motion: no-preference)'
    );
    let frame = null;
    let x = 0;
    let y = 0;

    function hide() {
        if (frame !== null) window.cancelAnimationFrame(frame);
        frame = null;
        spotlight.classList.remove('is-visible');
    }

    function paint() {
        frame = null;
        if (!enabled.matches || document.hidden) return;
        spotlight.style.transform = `translate3d(${x}px, ${y}px, 0) translate(-50%, -50%)`;
        spotlight.classList.add('is-visible');
    }

    function onPointerMove(event) {
        if (document.hidden || event.pointerType !== 'mouse') {
            hide();
            return;
        }
        x = event.clientX;
        y = event.clientY;
        if (frame === null) frame = window.requestAnimationFrame(paint);
    }

    document.documentElement.addEventListener('pointerleave', hide);
    window.addEventListener('blur', hide);
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) hide();
    });
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Tab') hide();
    });
    // Touch/reduced-motion devices do not need a mouse-movement listener at all.
    function syncPointerListener() {
        hide();
        document.removeEventListener('pointermove', onPointerMove);
        if (enabled.matches) {
            document.addEventListener('pointermove', onPointerMove, { passive: true });
        }
    }
    enabled.addEventListener('change', syncPointerListener);
    syncPointerListener();

    // Stop decorative animation when it is offscreen or the tab is hidden.
    if ('IntersectionObserver' in window) {
        const decorations = new Map();
        const syncAnimation = () => decorations.forEach((visible, element) => {
            element.classList.toggle('animation-paused', document.hidden || !visible);
        });
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => decorations.set(entry.target, entry.isIntersecting));
            syncAnimation();
        }, { rootMargin: '0px' });
        document.querySelectorAll('.liquid-orb, .swim-sphere').forEach((element) => {
            decorations.set(element, false);
            element.classList.add('animation-paused');
            observer.observe(element);
        });
        document.addEventListener('visibilitychange', syncAnimation);
    }
})();
