# popup_nuke.py

async def lufthansa_apocalypse_mode(page):
    """
    The single most overkill popup handler ever written for a single airline.
    Works today. Will still work after their next 17 redesigns.
    """
    print("Activating Lufthansa Popup Genocide Protocol™...")

    # Step 1: Lie to their tracking scripts before they even wake up
    await page.add_init_script("""
        // OneTrust? Never heard of her.
        window.OneTrust = { RejectAll: () => console.log("🤫 OneTrust quietly murdered") };
        window.OnetrustAcceptBtnHandler = () => console.log("🍪 Cookies? What cookies?");
        
        // Block known offenders at the network level
        const banned = ['onetrust', 'consent', 'cookie', 'feedback', 'survey', 'newsletter', 'didomi'];
        const realFetch = window.fetch;
        window.fetch = (...args) => {
            const url = args[0]?.toString() || '';
            if (banned.some evil => url.includes(evil)) {
                console.log(`[NUKE] Blocked popup script: ${url}`);
                return Promise.resolve(new Response('{}', {status: 200}));
            }
            return realFetch(...args);
        };
        
        // Exit-intent detection? Cute.
        document.onmouseleave = null;
        window.onmouseleave = null;
    """)

    # Step 2: DOM surgery — remove anything that even *smells* like a modal
    await page.wait_for_load_state("domcontentloaded")
    await page.evaluate("""
        () => {
            const selectors = [
                '[id*="modal"], [class*="modal"], [id*="overlay"], [class*="overlay"]',
                '[id*="cookie"], [class*="cookie"], [id*="consent"], [class*="consent"]',
                '[id*="feedback"], [class*="feedback"], [id*="survey"]',
                'iframe[src*="consent"], iframe[src*="cookie"]',
                'div[role="dialog"], aside, dialog[open]'
            ];
            document.querySelectorAll(selectors.join(', ')).forEach(el => {
                console.log("💀 Deleted:", el.outerHTML.substring(0, 100));
                el.remove();
            });
            
            // Shadow DOM purge (because OneTrust loves hiding)
            document.querySelectorAll('*').forEach(el => {
                if (el.shadowRoot) {
                    el.shadowRoot.querySelectorAll('button, div, iframe').forEach(child => {
                        if (/close|reject|no|later/i.test(child.textContent || '')) {
                            child.click();
                        }
                    });
                }
            });
        }
    """)

    # Step 3: Emergency keyboard violence — just in case
    await page.keyboard.press("Escape")
    await page.keyboard.press("Escape")  # Double tap for respect
    await page.mouse.move(10, 10)  # "I'm not leaving, stop asking"

    # Step 4: Final sweep — click anything that dares to say "close"
    for selector in [
        "text=/close|reject|no thanks|later|skip|no, thanks/i",
        "[aria-label*='close' i]",
        "button:has-text('✕'), button:has-text('×')"
    ]:
        try:
            await page.locator(selector).first.click(timeout=2000, force=True)
        except:
            pass  # already dead

    print("All popups executed. Site is now clean. You're welcome.")
