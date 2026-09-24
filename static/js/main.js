const menuToggle = document.getElementById("menuToggle");
const siteNav = document.getElementById("siteNav");

if (menuToggle && siteNav) {
    menuToggle.addEventListener("click", () => {
        const isOpen = siteNav.classList.toggle("is-open");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            siteNav.classList.remove("is-open");
            menuToggle.setAttribute("aria-expanded", "false");
        }
    });
}

const loginTrigger = document.getElementById("loginModalTrigger");
const loginModal = document.getElementById("loginModal");
const loginForm = document.getElementById("loginModalForm");
const loginError = document.getElementById("loginModalError");

if (loginTrigger && loginModal && loginForm) {
    const loginDialog = loginModal.querySelector(".sc-login-dialog");
    const usernameInput = document.getElementById("modalUsername");

    const openLogin = () => {
        loginModal.hidden = false;
        document.body.classList.add("sc-modal-open");
        loginError.hidden = true;
        loginDialog.focus();
        window.setTimeout(() => usernameInput.focus(), 0);
    };

    const closeLogin = () => {
        loginModal.hidden = true;
        document.body.classList.remove("sc-modal-open");
        loginTrigger.focus();
    };

    loginTrigger.addEventListener("click", (event) => {
        event.preventDefault();
        openLogin();
    });

    loginModal.querySelectorAll("[data-login-close]").forEach((button) => {
        button.addEventListener("click", closeLogin);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !loginModal.hidden) closeLogin();
    });

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = loginForm.querySelector("button[type=submit]");
        submitButton.disabled = true;
        loginError.hidden = true;

        try {
            const response = await fetch(loginForm.action, {
                method: "POST",
                body: new FormData(loginForm),
                headers: {"X-Requested-With": "XMLHttpRequest"},
            });
            const data = await response.json();
            if (!response.ok || !data.success) throw new Error(data.error || "Unable to log in.");
            window.location.assign(data.redirect || window.location.href);
        } catch (error) {
            loginError.textContent = error.message;
            loginError.hidden = false;
        } finally {
            submitButton.disabled = false;
        }
    });
}

const heroSlider = document.getElementById("homeHeroSlider");

if (heroSlider) {
    const heroSlides = [...heroSlider.querySelectorAll("[data-hero-slide]")];
    const heroDots = [...heroSlider.querySelectorAll("[data-hero-dot]")];
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let heroIndex = 0;
    let heroTimer;

    const showHeroSlide = (nextIndex) => {
        heroIndex = (nextIndex + heroSlides.length) % heroSlides.length;
        heroSlides.forEach((slide, index) => {
            const active = index === heroIndex;
            slide.classList.toggle("is-active", active);
            slide.setAttribute("aria-hidden", String(!active));
        });
        heroDots.forEach((dot, index) => {
            const active = index === heroIndex;
            dot.classList.toggle("is-active", active);
            dot.setAttribute("aria-current", String(active));
        });
    };

    const startHero = () => {
        if (reduceMotion) return;
        window.clearInterval(heroTimer);
        heroTimer = window.setInterval(() => showHeroSlide(heroIndex + 1), 5000);
    };

    heroDots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            showHeroSlide(index);
            startHero();
        });
    });

    heroSlider.addEventListener("mouseenter", () => window.clearInterval(heroTimer));
    heroSlider.addEventListener("mouseleave", startHero);
    startHero();
}

const cartToast = document.getElementById("cartToast");
const cartToastMessage = document.getElementById("cartToastMessage");
let cartToastTimer;

const showCartToast = (message) => {
    if (!cartToast) return;
    cartToastMessage.textContent = message;
    cartToast.hidden = false;
    window.requestAnimationFrame(() => cartToast.classList.add("is-visible"));
    window.clearTimeout(cartToastTimer);
    cartToastTimer = window.setTimeout(() => {
        cartToast.classList.remove("is-visible");
        window.setTimeout(() => { cartToast.hidden = true; }, 250);
    }, 3200);
};

document.querySelectorAll('a[href*="/cart/add/"]').forEach((link) => {
    link.addEventListener("click", async (event) => {
        event.preventDefault();
        if (link.dataset.cartPending === "true") return;
        link.dataset.cartPending = "true";
        link.classList.add("is-loading");

        try {
            const response = await fetch(link.href, {
                headers: {"X-Requested-With": "XMLHttpRequest"},
            });

            if (response.redirected && response.url.includes("/login/")) {
                const trigger = document.getElementById("loginModalTrigger");
                if (trigger) trigger.click();
                return;
            }

            const data = await response.json();
            if (!response.ok || !data.success) throw new Error("Unable to add this product.");

            document.querySelectorAll(".sc-cart-count").forEach((count) => {
                count.textContent = String(data.cart_count);
            });
            const cartLink = document.querySelector(".sc-cart-action");
            if (cartLink) cartLink.setAttribute("aria-label", `Cart: ${data.cart_count} items`);
            showCartToast(`${data.product_name} added successfully.`);
        } catch (error) {
            showCartToast(error.message);
        } finally {
            link.dataset.cartPending = "false";
            link.classList.remove("is-loading");
        }
    });
});

const comparePickerForm = document.querySelector(".sc-compare-picker-form");

if (comparePickerForm) {
    const pickerChecks = [...comparePickerForm.querySelectorAll('input[name="products"]')];
    const pickerError = comparePickerForm.querySelector(".sc-compare-picker-error");
    const selectionCount = comparePickerForm.querySelector("[data-selection-count]");
    const selectionHint = comparePickerForm.querySelector("[data-selection-hint]");
    const floatingButton = comparePickerForm.querySelector(".sc-floating-compare");
    const floatingCount = comparePickerForm.querySelector("[data-floating-count]");

    const updateComparePicker = () => {
        const selected = pickerChecks.filter((item) => item.checked);
        const activeCategory = selected[0]?.dataset.category || "";
        const categoryLabel = activeCategory ? activeCategory.charAt(0).toUpperCase() + activeCategory.slice(1) : "";

        pickerChecks.forEach((item) => {
            const isOtherCategory = Boolean(activeCategory && item.dataset.category !== activeCategory);
            item.disabled = isOtherCategory;
            item.closest(".sc-compare-pick-card")?.classList.toggle("is-category-locked", isOtherCategory);
        });

        selectionCount.textContent = `${selected.length} product${selected.length === 1 ? "" : "s"} selected`;
        selectionHint.textContent = activeCategory
            ? `${categoryLabel} comparison · choose ${selected.length < 2 ? "at least one more" : "up to three products"}.`
            : "Select a mobile or laptop to begin.";
        floatingCount.textContent = String(selected.length);
        floatingButton.disabled = selected.length < 2 || selected.length > 3;
        floatingButton.classList.toggle("is-visible", selected.length >= 1);
    };

    pickerChecks.forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            const selected = pickerChecks.filter((item) => item.checked);
            if (selected.length > 3) {
                checkbox.checked = false;
                pickerError.textContent = "You can compare a maximum of three products.";
                pickerError.hidden = false;
            } else {
                pickerError.hidden = true;
            }
            updateComparePicker();
        });
    });

    comparePickerForm.addEventListener("submit", (event) => {
        const selectedCount = pickerChecks.filter((item) => item.checked).length;
        if (selectedCount < 2 || selectedCount > 3) {
            event.preventDefault();
            pickerError.textContent = "Please select two or three products from the same category.";
            pickerError.hidden = false;
        }
    });

    updateComparePicker();
}
