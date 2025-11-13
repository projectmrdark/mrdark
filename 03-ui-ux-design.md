# Mr.Dark AI Agent Platform - UI/UX Design & Component Structure

## 1. Design Philosophy

### 1.1 Core Principles

1. **Simplicity First** - เรียบง่ายแบบ ChatGPT, ไม่ซับซ้อน
2. **Professional Look** - ไม่ใช้อีโมจิมากเกินไป, ดูเป็นมืออาชีพ
3. **Powerful Visibility** - แสดงผลการทำงานแบบ Manus (Sandbox, Tools, Browser)
4. **Responsive** - ใช้งานได้ทุกอุปกรณ์ (Desktop, Tablet, Mobile)
5. **Dark Mode First** - เริ่มต้นด้วย Dark theme (มี Light mode option)
6. **Fast & Smooth** - โหลดเร็ว, animation ลื่นไหล
7. **Accessibility** - รองรับ screen readers, keyboard navigation

### 1.2 Design References

**Inspiration from ChatGPT:**
- Clean chat interface
- Simple input area
- Minimal sidebar
- Clear message separation
- Smooth streaming

**Inspiration from Manus:**
- Tool execution visibility
- File explorer
- Browser viewer
- Code editor integration
- Real-time status updates

**Unique to Mr.Dark:**
- Dual mode indicator (Sandbox/Local)
- Quota display
- API key management
- Advanced settings

## 2. Color Palette

### 2.1 Dark Theme (Default)

```css
/* Primary Colors */
--bg-primary: #0A0A0A;          /* Main background */
--bg-secondary: #1A1A1A;        /* Secondary background */
--bg-tertiary: #2A2A2A;         /* Tertiary background */
--bg-hover: #333333;            /* Hover state */

/* Text Colors */
--text-primary: #FFFFFF;        /* Primary text */
--text-secondary: #A0A0A0;      /* Secondary text */
--text-tertiary: #707070;       /* Tertiary text */
--text-disabled: #505050;       /* Disabled text */

/* Accent Colors */
--accent-primary: #8B5CF6;      /* Purple - Primary brand */
--accent-secondary: #3B82F6;    /* Blue - Links, info */
--accent-success: #10B981;      /* Green - Success */
--accent-warning: #F59E0B;      /* Orange - Warning */
--accent-error: #EF4444;        /* Red - Error */

/* Borders */
--border-primary: #333333;      /* Primary border */
--border-secondary: #2A2A2A;    /* Secondary border */

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.5);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
```

### 2.2 Light Theme

```css
/* Primary Colors */
--bg-primary: #FFFFFF;
--bg-secondary: #F9FAFB;
--bg-tertiary: #F3F4F6;
--bg-hover: #E5E7EB;

/* Text Colors */
--text-primary: #111827;
--text-secondary: #6B7280;
--text-tertiary: #9CA3AF;
--text-disabled: #D1D5DB;

/* Accent Colors */
--accent-primary: #8B5CF6;
--accent-secondary: #3B82F6;
--accent-success: #10B981;
--accent-warning: #F59E0B;
--accent-error: #EF4444;

/* Borders */
--border-primary: #E5E7EB;
--border-secondary: #F3F4F6;

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
```

## 3. Typography

### 3.1 Font Families

```css
/* Primary Font - UI */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monospace Font - Code */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

/* Display Font - Logo */
--font-display: 'Inter', sans-serif;
```

### 3.2 Font Sizes

```css
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */
```

### 3.3 Font Weights

```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

## 4. Layout Structure

### 4.1 Overall Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                        Top Navigation Bar                        │
│  [Logo] [Mode Toggle] [Model Selector]    [Quota] [Settings] [User]
├─────────────┬───────────────────────────────────────────────────┤
│             │                                                     │
│  Sidebar    │              Main Content Area                     │
│             │                                                     │
│  [+ New]    │  ┌─────────────────────────────────────────────┐  │
│             │  │                                               │  │
│  Sessions:  │  │         Chat Messages Area                   │  │
│  • Chat 1   │  │         (Scrollable)                         │  │
│  • Chat 2   │  │                                               │  │
│  • Chat 3   │  │                                               │  │
│             │  └─────────────────────────────────────────────┘  │
│             │  ┌─────────────────────────────────────────────┐  │
│  [Archive]  │  │         Input Area                           │  │
│  [Settings] │  │  [Attach] [Text Input...]        [Send]      │  │
│             │  └─────────────────────────────────────────────┘  │
│             │                                                     │
├─────────────┴───────────────────────────────────────────────────┤
│              Execution Viewer Panel (Collapsible)                │
│  [Tools] [Browser] [Files] [Terminal] [Network]                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 640px) { /* sm */ }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { /* md */ }

/* Desktop */
@media (min-width: 1025px) { /* lg */ }

/* Large Desktop */
@media (min-width: 1440px) { /* xl */ }
```

### 4.3 Layout Behavior

**Desktop (>1024px):**
- Sidebar: Fixed width 280px, always visible
- Main content: Flexible width
- Execution viewer: Bottom panel, collapsible

**Tablet (641-1024px):**
- Sidebar: Collapsible, overlay on main content
- Main content: Full width when sidebar hidden
- Execution viewer: Bottom panel, collapsible

**Mobile (<640px):**
- Sidebar: Full-screen overlay
- Main content: Full width
- Execution viewer: Full-screen modal

## 5. Component Specifications

### 5.1 Top Navigation Bar

**Component: TopNav**

```tsx
<TopNav>
  <Logo />
  <ModeToggle /> {/* Sandbox / Local */}
  <ModelSelector /> {/* GPT-4, Claude, etc. */}
  <Spacer />
  <QuotaDisplay />
  <SettingsButton />
  <UserMenu />
</TopNav>
```

**Specifications:**
- Height: 64px
- Background: `--bg-secondary`
- Border bottom: 1px `--border-primary`
- Padding: 0 24px
- Items: Flex row, align center

**Logo:**
- Text: "Mr.Dark"
- Font: `--font-display`, `--text-2xl`, `--font-bold`
- Color: `--accent-primary`
- Icon: Dark moon/star symbol (minimal)

**Mode Toggle:**
- Type: Segmented control
- Options: "Sandbox" | "Local"
- Active: `--accent-primary` background
- Inactive: `--bg-tertiary`
- Width: 200px

**Model Selector:**
- Type: Dropdown
- Options: GPT-4, GPT-4 Turbo, Claude 3 Opus, Gemini Pro, etc.
- Width: 180px
- Icon: Model provider logo (small)

**Quota Display:**
- Format: "1.2M / 1M tokens"
- Color: Green if <80%, Orange if 80-95%, Red if >95%
- Tooltip: Detailed breakdown on hover

**User Menu:**
- Avatar: Circle, 40px
- Dropdown: Profile, Settings, API Keys, Logout

### 5.2 Sidebar

**Component: Sidebar**

```tsx
<Sidebar>
  <NewChatButton />
  <SessionList>
    <SessionGroup label="Today">
      <SessionItem />
      <SessionItem />
    </SessionGroup>
    <SessionGroup label="Yesterday">
      <SessionItem />
    </SessionGroup>
    <SessionGroup label="Last 7 Days">
      <SessionItem />
    </SessionGroup>
  </SessionList>
  <SidebarFooter>
    <ArchiveButton />
    <SettingsButton />
  </SidebarFooter>
</Sidebar>
```

**Specifications:**
- Width: 280px (desktop), 100% (mobile overlay)
- Background: `--bg-secondary`
- Border right: 1px `--border-primary`
- Padding: 16px

**New Chat Button:**
- Full width
- Height: 44px
- Background: `--accent-primary`
- Text: "+ New Chat"
- Icon: Plus icon
- Hover: Slightly lighter

**Session Item:**
- Height: 48px
- Padding: 12px 16px
- Border radius: 8px
- Hover: `--bg-hover`
- Active: `--bg-tertiary` + left border `--accent-primary`
- Text: Session title (truncate)
- Right icon: More options (3 dots)

**Session Group:**
- Label: `--text-tertiary`, `--text-xs`, uppercase
- Margin: 16px 0 8px 0

### 5.3 Chat Messages Area

**Component: ChatMessages**

```tsx
<ChatMessages>
  <MessageList>
    <Message role="user" />
    <Message role="assistant" />
    <Message role="user" />
    <Message role="assistant" streaming />
  </MessageList>
  <ScrollToBottom />
</ChatMessages>
```

**Specifications:**
- Background: `--bg-primary`
- Padding: 24px
- Max width: 800px (centered)
- Overflow: Auto scroll

**Message (User):**
- Align: Right
- Background: `--bg-tertiary`
- Border radius: 16px
- Padding: 12px 16px
- Max width: 70%
- Text color: `--text-primary`

**Message (Assistant):**
- Align: Left
- Background: Transparent
- Padding: 12px 0
- Max width: 100%
- Text color: `--text-primary`
- Avatar: Mr.Dark logo (small, 32px)

**Message Content:**
- Markdown rendering
- Code blocks: Syntax highlighting
- Images: Max width 100%, rounded corners
- Links: `--accent-secondary`, underline on hover
- Tables: Bordered, striped rows

**Streaming Indicator:**
- Cursor: Blinking vertical line
- Animation: Fade in/out 1s

**Message Actions:**
- Copy button (code blocks)
- Regenerate (assistant messages)
- Edit (user messages)
- Delete

### 5.4 Input Area

**Component: ChatInput**

```tsx
<ChatInput>
  <AttachButton />
  <TextArea placeholder="Message Mr.Dark..." />
  <SendButton />
  <AttachmentPreview />
</ChatInput>
```

**Specifications:**
- Background: `--bg-secondary`
- Border: 1px `--border-primary`
- Border radius: 12px
- Padding: 12px 16px
- Min height: 56px
- Max height: 200px (auto-expand)

**Text Area:**
- Background: Transparent
- Border: None
- Font: `--font-sans`, `--text-base`
- Color: `--text-primary`
- Placeholder: `--text-tertiary`
- Resize: Vertical auto
- Focus: Border color `--accent-primary`

**Attach Button:**
- Icon: Paperclip
- Size: 24px
- Color: `--text-secondary`
- Hover: `--text-primary`

**Send Button:**
- Icon: Arrow up
- Size: 40px
- Background: `--accent-primary`
- Border radius: 50%
- Disabled: `--bg-tertiary` (when input empty)
- Hover: Slightly lighter

**Attachment Preview:**
- Position: Above input
- Layout: Horizontal scroll
- Item: Thumbnail + filename + remove button
- Max items: 10

### 5.5 Execution Viewer Panel

**Component: ExecutionViewer**

```tsx
<ExecutionViewer>
  <TabBar>
    <Tab icon="tools" label="Tools" />
    <Tab icon="browser" label="Browser" />
    <Tab icon="files" label="Files" />
    <Tab icon="terminal" label="Terminal" />
    <Tab icon="network" label="Network" />
  </TabBar>
  <TabContent>
    {activeTab === 'tools' && <ToolsPanel />}
    {activeTab === 'browser' && <BrowserPanel />}
    {activeTab === 'files' && <FilesPanel />}
    {activeTab === 'terminal' && <TerminalPanel />}
    {activeTab === 'network' && <NetworkPanel />}
  </TabContent>
  <ResizeHandle />
</ExecutionViewer>
```

**Specifications:**
- Position: Bottom of screen
- Height: 300px (default), resizable 200-600px
- Background: `--bg-secondary`
- Border top: 1px `--border-primary`
- Collapsible: Click tab bar to collapse

**Tab Bar:**
- Height: 48px
- Background: `--bg-tertiary`
- Border bottom: 1px `--border-primary`
- Tabs: Horizontal layout

**Tab:**
- Padding: 12px 20px
- Active: Border bottom 2px `--accent-primary`
- Inactive: `--text-secondary`
- Hover: `--text-primary`

**Tools Panel:**
- Shows list of tool executions
- Each item: Tool name, status, timestamp, duration
- Expandable: Click to see details (params, result)
- Status colors: Running (blue), Success (green), Error (red)

**Browser Panel:**
- Screenshot viewer (latest screenshot)
- URL bar (current page)
- Navigation buttons (back, forward, refresh)
- DOM inspector (collapsible tree)

**Files Panel:**
- Tree view of session files
- Actions: Download, delete, rename
- Preview: Click to open in modal

**Terminal Panel:**
- Live terminal output
- Auto-scroll to bottom
- Copy button
- Clear button

**Network Panel:**
- List of HTTP requests
- Columns: Method, URL, Status, Time
- Click to see request/response details

### 5.6 Settings Modal

**Component: SettingsModal**

```tsx
<SettingsModal>
  <ModalHeader>
    <Title>Settings</Title>
    <CloseButton />
  </ModalHeader>
  <ModalBody>
    <TabBar>
      <Tab>General</Tab>
      <Tab>API Keys</Tab>
      <Tab>Quota</Tab>
      <Tab>Advanced</Tab>
    </TabBar>
    <TabContent>
      {/* Tab-specific content */}
    </TabContent>
  </ModalBody>
  <ModalFooter>
    <CancelButton />
    <SaveButton />
  </ModalFooter>
</SettingsModal>
```

**General Tab:**
- Theme: Light / Dark / Auto
- Language: English / Thai / etc.
- Default Model: Dropdown
- Default Mode: Sandbox / Local
- Notifications: Toggle

**API Keys Tab:**
- List of user API keys
- Add new key: Provider, Key, Name
- Delete key: Confirmation dialog
- Test key: Validate button

**Quota Tab:**
- Current usage: Progress bar
- Monthly limit: Display
- Reset date: Display
- Usage history: Chart (last 30 days)
- Upgrade button (if free tier)

**Advanced Tab:**
- Temperature: Slider (0-2)
- Max tokens: Input
- Top P: Slider (0-1)
- Frequency penalty: Slider (-2 to 2)
- Presence penalty: Slider (-2 to 2)

### 5.7 Local Client Setup Modal

**Component: LocalClientSetup**

```tsx
<LocalClientSetup>
  <Steps>
    <Step number={1} title="Download Client" />
    <Step number={2} title="Install & Run" />
    <Step number={3} title="Connect" />
  </Steps>
  <StepContent>
    {step === 1 && <DownloadStep />}
    {step === 2 && <InstallStep />}
    {step === 3 && <ConnectStep />}
  </StepContent>
  <StepActions>
    <BackButton />
    <NextButton />
  </StepActions>
</LocalClientSetup>
```

**Download Step:**
- Platform selection: Windows / macOS / Linux
- Download button (large, prominent)
- System requirements

**Install Step:**
- Installation instructions (OS-specific)
- Screenshots/GIFs
- Troubleshooting link

**Connect Step:**
- Token display (copy button)
- Connection status indicator
- Reconnect button

## 6. User Flows

### 6.1 First-Time User Flow

```
1. User visits website
   ↓
2. Landing page (hero, features, CTA)
   ↓
3. Click "Get Started" → Sign up modal
   ↓
4. Enter email + password → Create account
   ↓
5. Welcome modal (quick tour)
   ↓
6. First chat screen (empty state)
   ↓
7. Prompt: "Try asking me to..."
   ↓
8. User sends first message
   ↓
9. AI responds with tool execution
   ↓
10. Execution viewer opens automatically
   ↓
11. User sees tools in action
   ↓
12. Onboarding complete
```

### 6.2 Chat Flow (Sandbox Mode)

```
1. User types message + attaches file
   ↓
2. Click send button
   ↓
3. Message appears in chat (user)
   ↓
4. Loading indicator (assistant typing)
   ↓
5. AI response starts streaming
   ↓
6. AI decides to use tool (e.g., read file)
   ↓
7. Tool execution appears in viewer
   ↓
8. Tool status: Running → Completed
   ↓
9. AI continues response with results
   ↓
10. Response completes
   ↓
11. User can regenerate, copy, or continue
```

### 6.3 Switch to Local Mode Flow

```
1. User clicks mode toggle → "Local"
   ↓
2. Check if local client connected
   ↓
3. If not connected:
   a. Show setup modal
   b. User downloads client
   c. User installs and runs
   d. User copies token
   e. Client connects
   f. Modal closes
   ↓
4. If connected:
   a. Mode switches immediately
   b. Toast: "Now using local execution"
   ↓
5. Next message uses local client
```

### 6.4 API Key Management Flow

```
1. User opens Settings → API Keys tab
   ↓
2. Click "Add API Key"
   ↓
3. Modal opens:
   a. Select provider (OpenAI, Anthropic, Google)
   b. Enter API key
   c. Enter friendly name (optional)
   ↓
4. Click "Test Key"
   ↓
5. System validates key
   ↓
6. If valid:
   a. Key saved (encrypted)
   b. Toast: "API key added successfully"
   c. Modal closes
   ↓
7. If invalid:
   a. Error message
   b. User can retry
   ↓
8. Key appears in list
   ↓
9. User can delete or set as default
```

### 6.5 Quota Warning Flow

```
1. User sends message
   ↓
2. System checks quota
   ↓
3. If >80% used:
   a. Warning toast: "You've used 80% of your quota"
   ↓
4. If >95% used:
   a. Warning banner (persistent)
   b. "Upgrade" button prominent
   ↓
5. If quota exceeded:
   a. Block message sending
   b. Modal: "Quota exceeded"
   c. Options: Add own API key OR Upgrade
   ↓
6. User chooses:
   a. Add API key → API key flow
   b. Upgrade → Pricing page
```

## 7. Component Library

### 7.1 Base Components

**Button:**
- Variants: primary, secondary, ghost, danger
- Sizes: sm, md, lg
- States: default, hover, active, disabled, loading

**Input:**
- Types: text, email, password, number
- States: default, focus, error, disabled
- With icon support

**Select:**
- Single select
- Multi select
- Searchable
- With icons

**Checkbox:**
- Default
- Indeterminate
- Disabled

**Radio:**
- Default
- Disabled

**Switch:**
- Default
- Disabled

**Slider:**
- Single value
- Range
- With labels

**Textarea:**
- Auto-resize
- Character count
- Max length

**Modal:**
- Sizes: sm, md, lg, xl, full
- With overlay
- Closable
- Scrollable body

**Dropdown:**
- Menu items
- Dividers
- Icons
- Keyboard navigation

**Tooltip:**
- Positions: top, right, bottom, left
- Delay: 300ms

**Toast:**
- Types: info, success, warning, error
- Duration: 3s (configurable)
- Position: top-right (configurable)

**Badge:**
- Variants: default, primary, success, warning, error
- Sizes: sm, md, lg

**Avatar:**
- Sizes: xs, sm, md, lg, xl
- With fallback initials
- With status indicator

**Progress:**
- Linear
- Circular
- With label

**Skeleton:**
- Text
- Circle
- Rectangle
- Custom shapes

**Tabs:**
- Horizontal
- Vertical
- With icons

**Accordion:**
- Single expand
- Multiple expand
- With icons

**Card:**
- With header
- With footer
- Hoverable
- Clickable

### 7.2 Composite Components

**FileUpload:**
- Drag & drop
- Click to browse
- Multiple files
- File type restrictions
- Size limit
- Preview

**CodeBlock:**
- Syntax highlighting
- Line numbers
- Copy button
- Language label
- Collapsible (long code)

**MarkdownRenderer:**
- Full markdown support
- Code highlighting
- Tables
- Images
- Links
- Blockquotes

**DataTable:**
- Sortable columns
- Filterable
- Pagination
- Row selection
- Expandable rows

**Chart:**
- Line chart
- Bar chart
- Pie chart
- Area chart
- Responsive

**Timeline:**
- Vertical
- Horizontal
- With icons
- Collapsible items

**Breadcrumb:**
- With separators
- Clickable items
- Overflow handling

**Pagination:**
- With page numbers
- With prev/next
- With page size selector

**SearchBar:**
- With icon
- With clear button
- With suggestions
- Debounced

**CommandPalette:**
- Keyboard shortcut: Cmd+K
- Fuzzy search
- Grouped commands
- Recent commands

## 8. Animations & Transitions

### 8.1 Animation Principles

- **Purposeful**: Every animation serves a purpose
- **Fast**: Duration 150-300ms for most transitions
- **Smooth**: Use easing functions (ease-in-out)
- **Consistent**: Same animation for same actions
- **Subtle**: Not distracting

### 8.2 Common Animations

**Fade In/Out:**
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
/* Duration: 200ms */
```

**Slide In (from bottom):**
```css
@keyframes slideInUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
/* Duration: 250ms */
```

**Scale In:**
```css
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
/* Duration: 200ms */
```

**Skeleton Loading:**
```css
@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}
/* Duration: 2s, infinite */
```

**Typing Indicator:**
```css
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
/* Duration: 1s, infinite */
```

### 8.3 Page Transitions

- **Route change**: Fade in 200ms
- **Modal open**: Scale in + fade in 250ms
- **Modal close**: Scale out + fade out 200ms
- **Sidebar toggle**: Slide 300ms
- **Panel collapse**: Height transition 300ms

## 9. Accessibility

### 9.1 Keyboard Navigation

- **Tab**: Navigate between interactive elements
- **Enter/Space**: Activate buttons, links
- **Escape**: Close modals, dropdowns
- **Arrow keys**: Navigate lists, dropdowns
- **Cmd/Ctrl + K**: Open command palette
- **Cmd/Ctrl + N**: New chat
- **Cmd/Ctrl + /**: Focus input

### 9.2 Screen Reader Support

- **ARIA labels**: All interactive elements
- **ARIA roles**: Proper semantic roles
- **ARIA live regions**: For dynamic content
- **Alt text**: All images
- **Focus indicators**: Visible focus states

### 9.3 Color Contrast

- **Text**: Minimum 4.5:1 ratio (WCAG AA)
- **Large text**: Minimum 3:1 ratio
- **Interactive elements**: Minimum 3:1 ratio
- **Focus indicators**: Minimum 3:1 ratio

### 9.4 Font Sizes

- **Minimum**: 14px (0.875rem)
- **Body**: 16px (1rem)
- **Scalable**: Support browser zoom up to 200%

## 10. Responsive Design

### 10.1 Mobile Optimizations

**Navigation:**
- Hamburger menu for sidebar
- Bottom navigation for key actions
- Swipe gestures (open/close sidebar)

**Chat:**
- Full-width messages
- Larger tap targets (min 44px)
- Sticky input at bottom

**Execution Viewer:**
- Full-screen modal instead of panel
- Swipe down to close
- Tab bar at top

**File Upload:**
- Mobile-optimized file picker
- Camera access for photos
- Compress images before upload

### 10.2 Tablet Optimizations

**Layout:**
- Collapsible sidebar (overlay)
- Wider main content
- Split view option (chat + viewer side-by-side)

**Input:**
- Support for external keyboard
- Touch-optimized controls

### 10.3 Desktop Optimizations

**Layout:**
- Fixed sidebar
- Resizable panels
- Multi-column layouts (optional)

**Keyboard Shortcuts:**
- Full keyboard navigation
- Command palette
- Quick actions

**Mouse:**
- Hover states
- Context menus (right-click)
- Drag & drop

## 11. Loading States

### 11.1 Initial Load

```
1. Show splash screen (Mr.Dark logo)
   ↓
2. Load critical CSS
   ↓
3. Load React app
   ↓
4. Check authentication
   ↓
5. If authenticated:
   a. Load user data
   b. Load recent sessions
   c. Show main interface
   ↓
6. If not authenticated:
   a. Show landing page
```

### 11.2 Session Load

```
1. User clicks session
   ↓
2. Show skeleton for messages
   ↓
3. Load messages (paginated)
   ↓
4. Render messages
   ↓
5. Scroll to bottom
   ↓
6. Focus input
```

### 11.3 Message Send

```
1. User clicks send
   ↓
2. Disable input (prevent double-send)
   ↓
3. Show user message immediately
   ↓
4. Show typing indicator
   ↓
5. Stream AI response
   ↓
6. Enable input
```

### 11.4 Tool Execution

```
1. AI calls tool
   ↓
2. Show tool card in viewer
   ↓
3. Status: "Running" (spinner)
   ↓
4. Update progress (if applicable)
   ↓
5. Status: "Completed" (checkmark) or "Failed" (X)
   ↓
6. Show result summary
```

## 12. Error States

### 12.1 Network Error

```
┌─────────────────────────────────────┐
│  ⚠️  Connection Lost                │
│                                     │
│  Please check your internet         │
│  connection and try again.          │
│                                     │
│  [Retry]                            │
└─────────────────────────────────────┘
```

### 12.2 API Error

```
┌─────────────────────────────────────┐
│  ❌  Something went wrong           │
│                                     │
│  The AI service is temporarily      │
│  unavailable. Please try again.     │
│                                     │
│  [Retry]  [Report Issue]            │
└─────────────────────────────────────┘
```

### 12.3 Quota Exceeded

```
┌─────────────────────────────────────┐
│  🚫  Quota Exceeded                 │
│                                     │
│  You've used all your tokens        │
│  for this month.                    │
│                                     │
│  [Add API Key]  [Upgrade Plan]      │
└─────────────────────────────────────┘
```

### 12.4 File Upload Error

```
┌─────────────────────────────────────┐
│  ⚠️  Upload Failed                  │
│                                     │
│  File "document.pdf" is too large.  │
│  Maximum size: 10MB                 │
│                                     │
│  [Try Again]                        │
└─────────────────────────────────────┘
```

### 12.5 Sandbox Error

```
┌─────────────────────────────────────┐
│  ⚠️  Execution Failed               │
│                                     │
│  The sandbox encountered an error.  │
│  Please try again or switch to      │
│  local mode.                        │
│                                     │
│  [Retry]  [Switch to Local]         │
└─────────────────────────────────────┘
```

## 13. Empty States

### 13.1 No Sessions

```
┌─────────────────────────────────────┐
│                                     │
│         💬                          │
│                                     │
│    No conversations yet             │
│                                     │
│    Start a new chat to begin        │
│                                     │
│    [+ New Chat]                     │
│                                     │
└─────────────────────────────────────┘
```

### 13.2 No Files

```
┌─────────────────────────────────────┐
│                                     │
│         📁                          │
│                                     │
│    No files in this session         │
│                                     │
│    Upload files or generate them    │
│    with AI assistance               │
│                                     │
└─────────────────────────────────────┘
```

### 13.3 No API Keys

```
┌─────────────────────────────────────┐
│                                     │
│         🔑                          │
│                                     │
│    No API keys configured           │
│                                     │
│    Add your own API key to avoid    │
│    quota limits                     │
│                                     │
│    [+ Add API Key]                  │
│                                     │
└─────────────────────────────────────┘
```

## 14. Micro-interactions

### 14.1 Button Hover

- Scale: 1.02
- Brightness: +5%
- Transition: 150ms

### 14.2 Button Click

- Scale: 0.98
- Transition: 100ms

### 14.3 Input Focus

- Border color: `--accent-primary`
- Box shadow: 0 0 0 3px rgba(139, 92, 246, 0.1)
- Transition: 200ms

### 14.4 Message Appear

- Slide in from bottom
- Fade in
- Duration: 250ms

### 14.5 Tool Execution

- Pulse animation while running
- Checkmark animation on success
- Shake animation on error

### 14.6 Quota Bar

- Smooth width transition
- Color change based on percentage
- Pulse when near limit

## 15. Logo & Branding

### 15.1 Logo Design

**Concept:**
- Name: "Mr.Dark"
- Symbol: Minimalist dark moon or star
- Style: Modern, clean, professional
- Colors: Purple gradient (`#8B5CF6` to `#6D28D9`)

**Variations:**
- Full logo: Symbol + text
- Icon only: Symbol
- Text only: "Mr.Dark"

**Sizes:**
- Large: 200x200px (landing page)
- Medium: 64x64px (navigation)
- Small: 32x32px (favicon, avatar)

### 15.2 Favicon

- 32x32px icon
- Dark moon symbol
- Purple color
- Transparent background

### 15.3 Brand Voice

**Tone:**
- Professional but approachable
- Confident but not arrogant
- Helpful but not condescending
- Technical but not jargon-heavy

**Examples:**
- ✅ "I'll help you with that"
- ❌ "Let me do that for you"
- ✅ "Analyzing your data..."
- ❌ "Please wait while I process..."

## 16. Performance Targets

### 16.1 Load Times

- **First Contentful Paint**: <1.5s
- **Time to Interactive**: <3s
- **Largest Contentful Paint**: <2.5s

### 16.2 Runtime Performance

- **Frame Rate**: 60 FPS
- **Input Latency**: <100ms
- **Scroll Performance**: Smooth (no jank)

### 16.3 Bundle Size

- **Initial JS**: <200KB (gzipped)
- **Initial CSS**: <50KB (gzipped)
- **Total Initial**: <300KB (gzipped)

### 16.4 Optimization Strategies

- Code splitting by route
- Lazy loading components
- Image optimization (WebP, lazy load)
- Font subsetting
- Tree shaking
- Minification
- Compression (Brotli)

---

**Document Version**: 1.0  
**Last Updated**: 2024-01-XX  
**Status**: Draft - Pending Review
