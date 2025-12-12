# CarryOn Extension Setup Guide

## 🚀 Quick Setup

### 1. Extension is Ready to Use!
The extension now works with the live deployment at `https://carryon-summarizer.vercel.app` - no local server needed!

### 2. Install the Extension

#### Chrome/Edge/Brave:
1. Open `chrome://extensions` (or `edge://extensions`, `brave://extensions`)
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `carryon-extension` folder
5. The extension should appear in your extensions list

### 3. Configure the Extension (Optional)
The extension is pre-configured to work with the live deployment, but you can customize settings:
1. Click the CarryOn extension icon in your browser toolbar
2. Click "Settings" or expand the "Advanced" section
3. API Base URL is set to: `https://carryon-summarizer.vercel.app` (default)
4. Adjust target sentences or auto-size as needed
5. Click "Save" if you make changes

### 4. Test the Extension
1. Open the test page: `carryon-extension/test.html` in your browser
2. Select some text on the page
3. Click the CarryOn extension icon
4. Click "Grab Selection" - the text should appear in the input area
5. Click "Create Summary" - you should get a summary
6. Try "Copy" and "Download .txt" buttons

## 🔧 Troubleshooting

### ❌ "Failed to load resource: net::ERR_FILE_NOT_FOUND" (icon32.png)
**Fixed!** ✅ The extension now includes proper icon files in the `icons/` directory.

### ❌ "Failed to load resource: net::ERR_CONNECTION_REFUSED" (API)
**Solutions:**
1. Check your internet connection
2. Verify the API Base URL in extension settings: `https://carryon-summarizer.vercel.app`
3. Test the API directly: `https://carryon-summarizer.vercel.app/api/summarize`
4. If using localhost, make sure the server is running: `python run.py`

### ❌ Extension not appearing in browser
**Solutions:**
1. Make sure Developer Mode is enabled
2. Try refreshing the extensions page
3. Check for error messages in the extensions page
4. Ensure you selected the correct folder (`carryon-extension`)

### ❌ "Grab Selection" not working
**Solutions:**
1. Make sure you have text selected on the page
2. Try refreshing the page and selecting text again
3. Check browser console for JavaScript errors
4. Ensure the extension has proper permissions

### ❌ Auto-detection not working on AI sites
**Solutions:**
1. The extension works on: ChatGPT, Claude, Gemini, Copilot, Poe, Perplexity
2. Make sure you're on the actual chat page (not login/settings)
3. Wait for the page to fully load before opening the extension
4. Try refreshing the AI chat page

## 🌐 Supported Websites

### ✅ Auto-Detection Works On:
- **ChatGPT**: chat.openai.com
- **Claude**: claude.ai
- **Gemini**: gemini.google.com
- **Copilot**: copilot.microsoft.com, bing.com
- **Poe**: poe.com
- **Perplexity**: perplexity.ai

### ✅ Manual Selection Works On:
- Any website (select text and use "Grab Selection")

## 📋 Extension Features

### ✅ Working Features:
- ✅ Text selection and grabbing
- ✅ API communication with Flask server
- ✅ Text summarization
- ✅ Auto-size and manual sentence control
- ✅ Copy to clipboard
- ✅ Download as .txt file
- ✅ Settings persistence
- ✅ Auto-detection on AI chat sites
- ✅ Proper icon display
- ✅ CORS support

### 🔧 Settings:
- **API Base URL**: Server address (default: `https://carryon-summarizer.vercel.app`)
- **Auto size**: Automatically determine summary length
- **Target sentences**: Manual control (4-80 sentences)

## 🧪 Testing Checklist

- [ ] Server starts without errors
- [ ] Extension loads in browser
- [ ] Extension icon displays correctly
- [ ] Settings can be saved
- [ ] API Base URL is configured
- [ ] Text selection works
- [ ] "Grab Selection" populates input
- [ ] "Create Summary" generates summary
- [ ] "Copy" button works
- [ ] "Download .txt" button works
- [ ] Auto-detection works on AI sites
- [ ] No console errors

## 📞 Still Having Issues?

1. **Check server logs**: Look at the terminal where you started the server
2. **Check browser console**: F12 → Console tab for JavaScript errors
3. **Test API directly**: Visit `https://carryon-summarizer.vercel.app/api/summarize` in browser
4. **Verify extension permissions**: Check chrome://extensions page
5. **Try incognito mode**: Sometimes extensions behave differently

## 🎉 Success!

If everything is working, you should be able to:
- Select text on any webpage
- Get automatic summaries from AI chat sites
- Copy and download summaries
- Use the extension across different browsers and sites

The extension is now ready for production use!