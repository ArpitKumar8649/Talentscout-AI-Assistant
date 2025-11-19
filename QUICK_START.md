# 🚀 Quick Start - Deploy in 5 Minutes

## Fastest Way to Deploy Your App to Streamlit Cloud

---

## Step 1: Push to GitHub (2 minutes)

```bash
# 1. Create a new repository on GitHub
# Go to: https://github.com/new

# 2. Initialize and push (run these commands in /app directory)
cd /app
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

---

## Step 2: Deploy on Streamlit (2 minutes)

1. **Go to**: https://share.streamlit.io
2. **Sign in** with GitHub
3. **Click**: "New app"
4. **Fill in**:
   - Repository: `YOUR_USERNAME/YOUR_REPO_NAME`
   - Branch: `main`
   - Main file: `streamlit_app.py`
5. **Click**: "Deploy"

---

## Step 3: Add Secrets (1 minute)

1. In Streamlit dashboard, go to **Settings** → **Secrets**
2. **Paste this** (replace with your actual values):

```toml
LETTA_API_KEY = "your_letta_api_key"
LETTA_AGENT_ID = "agent-xxx-xxx-xxx"
LETTA_PROJECT_ID = "proj-xxx-xxx-xxx"
LETTA_BASE_URL = "https://api.letta.com"
```

3. **Click**: "Save"

---

## Step 4: Test Your App

Wait 2-3 minutes for deployment, then:
- Open your app URL: `https://YOUR-APP-NAME.streamlit.app`
- Verify "AI Agent Connected" shows in sidebar
- Test the chat: Type "Hello" and press Enter

---

## ✅ Done!

Your app is now live! 🎉

**Need more details?** See [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md)

---

## Troubleshooting

**Problem**: "Connection Error"  
**Fix**: Check your secrets in Streamlit dashboard

**Problem**: "Module not found"  
**Fix**: Dependencies are already in `requirements.txt` - should work automatically

**Problem**: "File not found"  
**Fix**: Make sure Main file path is set to `streamlit_app.py` (or `app/streamlit_app.py` if in subdirectory)

---

## Where to Get Letta Credentials

1. **API Key**: https://app.letta.com/ → Settings → API Keys
2. **Agent ID**: https://app.letta.com/ → Agents → (your agent) → Copy ID
3. **Project ID**: https://app.letta.com/ → Projects → Copy ID

---

## Support

- Streamlit Docs: https://docs.streamlit.io
- Letta Docs: https://docs.letta.com
- Community: https://discuss.streamlit.io
