import os

frontend_path = r"C:\Users\Nucom\Projects\MindGuard_AI\frontend\index.html"
root_index_path = r"C:\Users\Nucom\Projects\MindGuard_AI\index.html"

BULLETPROOF_CHAT_JS = """    let isChatBusy = false;

    async function sendChatMessage() {
      if (isChatBusy) return;
      const input = document.getElementById('chatInput');
      const sendBtn = document.getElementById('chatSendBtn');
      const text = input.value.trim();
      if (!text) return;

      isChatBusy = true;
      if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.innerHTML = "Thinking... &#9203;";
      }

      const chatBox = document.getElementById('chatMessages');
      const userBubble = document.createElement('div');
      userBubble.style = "max-width:85%; padding:0.85rem 1.1rem; border-radius:14px; font-size:0.9rem; background:linear-gradient(135deg, #2563EB, #1D4ED8); color:#fff; align-self:flex-end";
      userBubble.textContent = text;
      chatBox.appendChild(userBubble);
      input.value = '';
      chatBox.scrollTop = chatBox.scrollHeight;

      chatHistory.push({ role: 'user', content: text });

      // Typing Indicator
      const typingBubble = document.createElement('div');
      typingBubble.id = 'chatTypingIndicator';
      typingBubble.style = "max-width:85%; padding:0.75rem 1rem; border-radius:14px; font-size:0.85rem; background:var(--bg-card); border:1px solid var(--border); color:var(--text-muted); align-self:flex-start; display:flex; align-items:center; gap:0.5rem";
      typingBubble.innerHTML = `<span>MindBot Neural Brain is analyzing &amp; generating...</span> <span class="spinner" style="width:14px; height:14px; border:2px solid #3B82F6; border-top-color:transparent; border-radius:50%; display:inline-block; animation:spin 1s linear infinite"></span>`;
      chatBox.appendChild(typingBubble);
      chatBox.scrollTop = chatBox.scrollHeight;

      let data = null;
      const inf = runClientSideInference(text);
      const psych = calculateClientSidePsychometrics(text, chatHistory);
      const customKey = localStorage.getItem('mindguard_custom_api_key') || '';

      try {
        // Fast endpoint selection (try direct tunnel or local origin with 8s timeout)
        const targetUrl = window.location.hostname.includes("github.io") ? `${LIVE_BACKEND_TUNNEL}/api/chat` : "/api/chat";
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 8000);

        try {
          const resp = await fetch(targetUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: chatHistory.slice(-4), api_key: customKey }),
            signal: controller.signal
          });
          clearTimeout(timeoutId);
          if (resp.ok) {
            data = await resp.json();
          }
        } catch (fetchErr) {
          clearTimeout(timeoutId);
          console.warn("Primary API timeout/failed, trying direct neural fallback:", fetchErr);
        }

        // If backend was slow/offline and user provided custom key, call OpenRouter directly
        if ((!data || !data.reply) && customKey) {
          try {
            const systemPrompt = "You are MindGuard AI, an expert empathetic psychologist. Provide warm, concise, soothing advice.";
            const oRes = await fetch("https://openrouter.ai/api/v1/chat/completions", {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${customKey}`,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                model: "openrouter/free",
                messages: [{ role: "system", content: systemPrompt }, { role: "user", content: text }],
                max_tokens: 400
              })
            });
            if (oRes.ok) {
              const j = await oRes.json();
              data = {
                reply: j.choices[0].message.content,
                ai_brain_source: "OpenRouter Neural Brain (Direct User Key)",
                message_analysis: inf,
                psychometrics: psych
              };
            }
          } catch (e) {
            console.warn("Custom key direct call failed:", e);
          }
        }

        // Immediate situation-aware dynamic CBT fallback (Guaranteed < 5ms response, never hangs)
        if (!data || !data.reply) {
          const fallbackReply = generateClientSideEmpatheticResponse(text, inf, psych);
          data = {
            reply: fallbackReply,
            ai_brain_source: "Dynamic CBT Intelligence Engine (Ultra-Fast)",
            message_analysis: inf,
            psychometrics: psych,
            triage_recommendation: inf.risk_assessment ? inf.risk_assessment.clinical_recommendation : "Active Psychological Support"
          };
        }

        // Render Bot Bubble
        const botBubble = document.createElement('div');
        botBubble.style = "max-width:85%; padding:0.95rem 1.2rem; border-radius:14px; font-size:0.9rem; background:var(--bg-card); border:1px solid var(--border); color:var(--text-main); align-self:flex-start; line-height:1.55";
        botBubble.innerHTML = formatMarkdown(data.reply || "I am here with you. Please take a gentle breath.");
        chatBox.appendChild(botBubble);
        chatBox.scrollTop = chatBox.scrollHeight;

        chatHistory.push({ role: 'assistant', content: data.reply });

        // Update Calculating Power Telemetry HUD
        if (data.ai_brain_source) {
          const badge = document.getElementById('chatBrainBadge');
          if (badge) {
            badge.innerHTML = `&#9889; <strong>${data.ai_brain_source}</strong>`;
            badge.style.background = "rgba(16, 185, 129, 0.2)";
            badge.style.color = "#34D399";
            badge.style.borderColor = "#10B981";
          }
        }
        if (data.message_analysis) {
          const el = document.getElementById('chatLastClass');
          if (el) el.textContent = `${data.message_analysis.primary_class} (${data.message_analysis.confidence_percentage || 'Calculated'})`;
        }
        if (data.psychometrics) {
          const p = data.psychometrics;
          const vEl = document.getElementById('chatValence');
          if (vEl) {
            vEl.textContent = `${p.valence_score > 0 ? '+' : ''}${p.valence_score} (${p.valence_score > 0.2 ? 'Constructive' : p.valence_score < -0.3 ? 'Distress / Dysphoric' : 'Neutral'})`;
            vEl.style.color = p.valence_score > 0 ? '#10B981' : p.valence_score < -0.3 ? '#F87171' : '#38BDF8';
          }

          const aEl = document.getElementById('chatArousal');
          if (aEl) aEl.textContent = p.arousal_index;
          const aBar = document.getElementById('chatArousalBar');
          if (aBar) {
            const aVal = parseInt(p.arousal_index) || 35;
            aBar.style.width = `${aVal}%`;
          }

          const distContainer = document.getElementById('chatDistortions');
          if (distContainer) {
            distContainer.innerHTML = '';
            (p.distortions_detected || []).forEach(d => {
              const b = document.createElement('span');
              b.className = 'badge';
              b.style = "background:rgba(239, 68, 68, 0.15); color:#FCA5A5; border:1px solid rgba(239, 68, 68, 0.3); font-size:0.72rem; padding:0.2rem 0.5rem; border-radius:4px";
              b.textContent = d;
              distContainer.appendChild(b);
            });
          }

          const trajEl = document.getElementById('chatTrajectory');
          if (trajEl) {
            trajEl.textContent = p.trajectory;
            trajEl.style.color = p.trajectory.includes('Improving') ? '#10B981' : p.trajectory.includes('Escalating') ? '#EF4444' : '#38BDF8';
          }

          const prescEl = document.getElementById('chatPrescription');
          if (prescEl) prescEl.textContent = p.prescribed_soothing;
        }

      } catch (fatalErr) {
        console.error("Fatal chat error:", fatalErr);
        const errBubble = document.createElement('div');
        errBubble.style = "max-width:85%; padding:0.85rem 1.1rem; border-radius:14px; font-size:0.85rem; background:rgba(239, 68, 68, 0.15); border:1px solid #EF4444; color:#FCA5A5; align-self:flex-start";
        errBubble.textContent = "I am listening. Let's take a slow breath in for 4 seconds... and release for 6 seconds. What is one thought on your mind?";
        chatBox.appendChild(errBubble);
      } finally {
        // ALWAYS REMOVE TYPING INDICATOR AND RESTORE UI STATE (ZERO FREEZING)
        const tEl = document.getElementById('chatTypingIndicator');
        if (tEl) tEl.remove();

        isChatBusy = false;
        if (sendBtn) {
          sendBtn.disabled = false;
          sendBtn.innerHTML = "Send &#128330;&#65039;";
        }
        if (input) {
          input.focus();
        }
      }
    }"""

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        file_text = f.read()

    start_idx = file_text.find('    async function sendChatMessage()')
    end_idx = file_text.find('    // Clinical Questions Generator (PHQ-9 & GAD-7)')
    if start_idx != -1 and end_idx != -1:
        updated = file_text[:start_idx] + BULLETPROOF_CHAT_JS + "\n\n" + file_text[end_idx:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"[{path}] Bulletproof chat JS applied successfully!")
    else:
        print(f"[{path}] Boundary match failed: start={start_idx}, end={end_idx}")

update_file(frontend_path)
update_file(root_index_path)
