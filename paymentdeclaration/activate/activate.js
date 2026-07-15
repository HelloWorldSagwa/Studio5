import { createClient } from "https://esm.sh/@supabase/supabase-js@2.57.4";

const config = window.PAYMENT_DECLARATION_CONFIG;
const views = ["loading-view", "login-view", "activation-view", "success-view", "fatal-error"];

if (!config?.supabaseUrl || !config?.supabasePublishableKey) {
    throw new Error("Supabase browser configuration is missing.");
}

const supabase = createClient(config.supabaseUrl, config.supabasePublishableKey, {
    db: { schema: "schema_1" },
    auth: {
        flowType: "pkce",
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: false
    }
});

const elements = {
    appleLogin: document.querySelector("#apple-login"),
    kakaoLogin: document.querySelector("#kakao-login"),
    activationForm: document.querySelector("#activation-form"),
    promotionCode: document.querySelector("#promotion-code"),
    activateButton: document.querySelector("#activate-button"),
    formMessage: document.querySelector("#form-message"),
    accountName: document.querySelector("#account-name"),
    accountProvider: document.querySelector("#account-provider"),
    successDescription: document.querySelector("#success-description"),
    supporterBadge: document.querySelector("#supporter-badge"),
    fatalErrorMessage: document.querySelector("#fatal-error-message"),
    retryButton: document.querySelector("#retry-button")
};

function showView(id) {
    views.forEach((viewId) => {
        document.getElementById(viewId).hidden = viewId !== id;
    });
}

function setProviderButtonsDisabled(disabled) {
    elements.appleLogin.disabled = disabled;
    elements.kakaoLogin.disabled = disabled;
}

function providerLabel(user) {
    const provider = user?.app_metadata?.provider;
    if (provider === "apple") return "Apple";
    if (provider === "kakao") return "카카오";
    return "로그인 계정";
}

function formatActivationDescription(status) {
    if (status.access_kind === "lifetime") {
        return `${status.campaign_name ?? "평생 이용권"}이 이 계정에 적용되었습니다.`;
    }

    if (status.expires_at) {
        const expiresAt = new Intl.DateTimeFormat("ko-KR", {
            year: "numeric",
            month: "long",
            day: "numeric"
        }).format(new Date(status.expires_at));
        return `${status.campaign_name ?? "이용권"}을 ${expiresAt}까지 이용할 수 있습니다.`;
    }

    return `${status.campaign_name ?? "이용권"}이 이 계정에 적용되었습니다.`;
}

async function signIn(provider) {
    setProviderButtonsDisabled(true);
    try {
        const redirectTo = new URL("./", window.location.href);
        redirectTo.search = "";
        redirectTo.hash = "";

        const { error } = await supabase.auth.signInWithOAuth({
            provider,
            options: { redirectTo: redirectTo.toString() }
        });

        if (error) throw error;
    } catch (error) {
        setProviderButtonsDisabled(false);
        showFatalError(error, "로그인을 시작하지 못했어요.");
    }
}

async function exchangeOAuthCodeIfNeeded() {
    const url = new URL(window.location.href);
    const code = url.searchParams.get("code");
    const oauthError = url.searchParams.get("error_description") ?? url.searchParams.get("error");

    if (oauthError) {
        url.search = "";
        window.history.replaceState({}, document.title, url.toString());
        throw new Error(oauthError);
    }

    if (!code) return;

    const { error } = await supabase.auth.exchangeCodeForSession(code);
    url.search = "";
    window.history.replaceState({}, document.title, url.toString());
    if (error) throw error;
}

async function loadActivationStatus() {
    const { data, error } = await supabase.rpc("get_my_promotion_activation_status");
    if (error) throw error;
    return data;
}

async function renderAuthenticatedState(user) {
    const status = await loadActivationStatus();

    if (status.promotion_active) {
        elements.successDescription.textContent = formatActivationDescription(status);
        elements.supporterBadge.hidden = !status.is_founding_supporter;
        showView("success-view");
        return;
    }

    elements.accountName.textContent = status.nickname || status.user_code || "결제선언 사용자";
    elements.accountProvider.textContent = providerLabel(user);
    elements.formMessage.hidden = true;
    showView("activation-view");
    requestAnimationFrame(() => elements.promotionCode.focus({ preventScroll: true }));
}

async function initialize() {
    showView("loading-view");
    try {
        await exchangeOAuthCodeIfNeeded();
        const { data, error } = await supabase.auth.getUser();

        if (error && !String(error.message).toLowerCase().includes("session")) {
            throw error;
        }

        if (!data.user) {
            showView("login-view");
            return;
        }

        await renderAuthenticatedState(data.user);
    } catch (error) {
        showFatalError(error, "계정 정보를 불러오지 못했어요.");
    }
}

function showFatalError(error, fallback) {
    console.error(error);
    elements.fatalErrorMessage.textContent = fallback;
    showView("fatal-error");
}

function normalizeCodeInput(value) {
    const compact = value.toUpperCase().replace(/[^A-Z0-9]/g, "");
    if (!compact.startsWith("PD")) return value.toUpperCase();

    const payload = compact.slice(2, 22);
    const groups = payload.match(/.{1,4}/g) ?? [];
    return ["PD", ...groups].join("-");
}

elements.appleLogin.addEventListener("click", () => signIn("apple"));
elements.kakaoLogin.addEventListener("click", () => signIn("kakao"));

elements.promotionCode.addEventListener("input", (event) => {
    const formatted = normalizeCodeInput(event.target.value);
    if (formatted !== event.target.value) event.target.value = formatted;
    elements.formMessage.hidden = true;
});

elements.activationForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const code = elements.promotionCode.value.trim();

    if (!code) {
        elements.formMessage.textContent = "프로모션 코드를 입력해 주세요.";
        elements.formMessage.hidden = false;
        elements.promotionCode.focus();
        return;
    }

    elements.activateButton.disabled = true;
    elements.activateButton.textContent = "확인 중…";
    elements.formMessage.hidden = true;

    try {
        const { data, error } = await supabase.rpc("redeem_promotion_code", { p_code: code });
        if (error) throw error;

        if (!data?.success) {
            elements.formMessage.textContent = data?.message ?? "코드를 활성화하지 못했어요.";
            elements.formMessage.hidden = false;
            return;
        }

        elements.successDescription.textContent = formatActivationDescription(data);
        elements.supporterBadge.hidden = !data.is_founding_supporter;
        showView("success-view");
    } catch (error) {
        console.error(error);
        elements.formMessage.textContent = "코드를 확인하지 못했어요. 잠시 후 다시 시도해 주세요.";
        elements.formMessage.hidden = false;
    } finally {
        elements.activateButton.disabled = false;
        elements.activateButton.textContent = "코드 활성화";
    }
});

document.querySelectorAll("[data-logout]").forEach((button) => {
    button.addEventListener("click", async () => {
        button.disabled = true;
        await supabase.auth.signOut({ scope: "local" });
        window.location.replace(new URL("./", window.location.href));
    });
});

elements.retryButton.addEventListener("click", () => window.location.reload());

initialize();
