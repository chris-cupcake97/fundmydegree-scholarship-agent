import {
  ArrowLeft,
  BarChart3,
  BookOpen,
  Bookmark,
  BriefcaseBusiness,
  CalendarDays,
  CheckCircle2,
  ChevronDown,
  CircleHelp,
  ExternalLink,
  FileText,
  Globe2,
  GraduationCap,
  Heart,
  Landmark,
  LockKeyhole,
  MapPin,
  Pencil,
  Search,
  ShieldCheck,
  Sparkles,
  Star,
  UserRound,
  WalletCards,
  XCircle
} from "lucide-react";
import { FormEvent, ReactNode, useMemo, useState } from "react";
import {
  createProfile,
  draftEmail,
  getAudit,
  getEvidence,
  getSavedResults,
  saveResult,
  searchScholarships,
  verifyScholarship
} from "./api";
import type {
  AuditEvent,
  CandidateResult,
  Evidence,
  Rule,
  SavedResult,
  ScholarshipCandidate,
  StudentProfile,
  VerdictStatus,
  Verification
} from "./types";

type Screen = "profile" | "find" | "checker" | "saved";

const documentOptions = [
  ["transcript", "Transcript"],
  ["degree certificate", "Degree certificate"],
  ["grading scale", "Grading scale"],
  ["CV", "CV / Resume"],
  ["SOP", "Statement of Purpose"],
  ["reference letters", "Reference letters"],
  ["English test", "English test score"],
  ["passport", "Passport"],
  ["offer letter", "Other document"]
];

const navItems: Array<{ id: Screen; label: string; icon: JSX.Element }> = [
  { id: "profile", label: "My Profile", icon: <UserRound size={24} /> },
  { id: "find", label: "My Matches", icon: <Star size={24} /> },
  { id: "saved", label: "Saved", icon: <Heart size={24} /> }
];

const statusMeta: Record<
  VerdictStatus,
  { label: string; section: string; className: string; icon: JSX.Element }
> = {
  eligible: {
    label: "Strong match",
    section: "Best Matches",
    className: "status-eligible",
    icon: <Sparkles size={18} />
  },
  unclear: {
    label: "Need to Confirm",
    section: "Need to Confirm",
    className: "status-unclear",
    icon: <CircleHelp size={18} />
  },
  not_eligible: {
    label: "Not for You",
    section: "Not for You",
    className: "status-not-eligible",
    icon: <XCircle size={18} />
  },
  unverified: {
    label: "Couldn't Verify Yet",
    section: "Couldn't Verify Yet",
    className: "status-unverified",
    icon: <Search size={18} />
  }
};

const defaultProfile: StudentProfile = {
  nationality: "Sri Lanka",
  residence: "Sri Lanka",
  fee_status: "international",
  degree_level: "Master's",
  field: "Artificial Intelligence",
  intake: "2026/27",
  target_regions: ["Europe", "United Kingdom", "Germany", "Sweden", "Finland"],
  funding_need_percent: 40,
  need_living_stipend: true,
  academic_level: "upper second equivalent",
  work_experience_years: 1,
  research_experience: false,
  documents_available: ["CV", "transcript"]
};

function App() {
  const [screen, setScreen] = useState<Screen>("profile");
  const [profile, setProfile] = useState<StudentProfile>(defaultProfile);
  const [savedProfile, setSavedProfile] = useState<StudentProfile | null>(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<CandidateResult[]>([]);
  const [selected, setSelected] = useState<CandidateResult | null>(null);
  const [evidence, setEvidence] = useState<Evidence | null>(null);
  const [auditLog, setAuditLog] = useState<AuditEvent[]>([]);
  const [savedResults, setSavedResults] = useState<SavedResult[]>([]);
  const [busy, setBusy] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const grouped = useMemo(() => {
    const groups: Record<VerdictStatus, CandidateResult[]> = {
      eligible: [],
      unclear: [],
      not_eligible: [],
      unverified: []
    };
    for (const result of results) {
      groups[result.verification?.status ?? "unverified"].push(result);
    }
    return groups;
  }, [results]);

  const profileChips = savedProfile
    ? [
        ["From", savedProfile.nationality],
        ["Degree", savedProfile.degree_level],
        ["Subject", savedProfile.field],
        ["Funding", `${savedProfile.funding_need_percent}%+`],
        ["Region", displayRegion(savedProfile.target_regions)]
      ]
    : [];

  const activeNav = screen === "checker" ? "find" : screen;

  function setField<K extends keyof StudentProfile>(field: K, value: StudentProfile[K]) {
    setProfile((current) => ({ ...current, [field]: value }));
  }

  function toggleDocument(name: string) {
    setProfile((current) => {
      const exists = current.documents_available.includes(name);
      return {
        ...current,
        documents_available: exists
          ? current.documents_available.filter((document) => document !== name)
          : [...current.documents_available, name]
      };
    });
  }

  async function withBusy(label: string, action: () => Promise<void>) {
    setBusy(label);
    setError("");
    setNotice("");
    try {
      await action();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setBusy("");
    }
  }

  async function fetchMatches(profileForSearch: StudentProfile, searchQuery = query) {
    const search = await searchScholarships(profileForSearch.id!, searchQuery);
    const verifiedResults = await Promise.all(
      search.candidates.map(async (candidate) => {
        const verification = await verifyScholarship(profileForSearch.id!, candidate);
        return { candidate, verification: verification.verification };
      })
    );
    verifiedResults.sort(compareDemoResults);
    setResults(verifiedResults);
    setSelected(verifiedResults.find((item) => item.verification?.status === "eligible") ?? verifiedResults[0] ?? null);
    return verifiedResults;
  }

  async function submitProfile(event: FormEvent) {
    event.preventDefault();
    await withBusy("Finding matches", async () => {
      const response = await createProfile(profile);
      setSavedProfile(response.profile);
      const verifiedResults = await fetchMatches(response.profile);
      setNotice(`${verifiedResults.length} scholarships matched against your profile.`);
      setScreen("find");
    });
  }

  async function runSearch() {
    if (!savedProfile?.id) {
      setError("Save your profile first so we can match scholarships to you.");
      setScreen("profile");
      return;
    }

    await withBusy("Finding matches", async () => {
      const verifiedResults = await fetchMatches(savedProfile);
      setNotice(`${verifiedResults.length} scholarships matched against your profile.`);
    });
  }

  function upsertResult(next: CandidateResult) {
    setResults((current) =>
      current.map((item) => (item.candidate.id === next.candidate.id ? next : item))
    );
  }

  async function verifyAndReturn(result: CandidateResult): Promise<CandidateResult> {
    if (!savedProfile?.id) {
      setError("Save your profile first so we can check this scholarship against it.");
      setScreen("profile");
      return result;
    }
    const response = await verifyScholarship(savedProfile.id, result.candidate);
    const next = { ...result, verification: response.verification };
    upsertResult(next);
    return next;
  }

  async function openScholarship(result: CandidateResult) {
    const withVerification = result.verification ? result : await verifyAndReturn(result);
    if (!withVerification.verification) return;

    await withBusy("Opening match", async () => {
      const [evidenceResponse, auditResponse] = await Promise.all([
        getEvidence(withVerification.verification!.id),
        getAudit(withVerification.verification!.id)
      ]);
      setSelected(withVerification);
      setEvidence(evidenceResponse);
      setAuditLog(auditResponse.audit_log);
      setScreen("checker");
    });
  }

  async function saveCurrentResult(result: CandidateResult | null = selected) {
    if (!savedProfile?.id || !result?.verification) return;
    await withBusy("Saving scholarship", async () => {
      await saveResult(result.verification!.id, savedProfile.id!, "Saved from FundMyDegree.");
      await refreshSavedResults();
      setNotice("Scholarship saved.");
    });
  }

  async function refreshSavedResults() {
    if (!savedProfile?.id) return;
    const response = await getSavedResults(savedProfile.id);
    setSavedResults(response.saved_results);
  }

  async function goSavedResults() {
    await withBusy("Loading saved scholarships", async () => {
      await refreshSavedResults();
      setScreen("saved");
    });
  }

  async function openDraft(result: CandidateResult | null = selected) {
    if (!result?.verification) return;
    if (result.verification.status !== "unclear") {
      setNotice("Ask to confirm is available only when important scholarship details are unclear.");
      return;
    }

    await withBusy("Preparing draft", async () => {
      const draft = await draftEmail(result.verification!.id, "Demo Student", "Scholarship Office");
      setNotice(`Draft ready: ${draft.subject}`);
    });
  }

  function removeSavedResult(savedId: string) {
    setSavedResults((current) => current.filter((saved) => saved.id !== savedId));
    setNotice("Removed from this saved list.");
  }

  return (
    <div className="app-shell">
      <Sidebar
        active={activeNav}
        onNavigate={(next) => {
          if (next === "saved") void goSavedResults();
          else setScreen(next);
        }}
      />

      <main className={`main stage-${screen}`}>
        <Hero screen={screen} onBack={() => setScreen("find")} />

        {(notice || error) && (
          <div className={`message ${error ? "message-error" : "message-info"}`}>
            {error || notice}
          </div>
        )}

        {screen === "profile" && (
          <ProfileWizard
            profile={profile}
            onSubmit={submitProfile}
            onField={setField}
            onToggleDocument={toggleDocument}
          />
        )}

        {screen === "find" && (
          <FindScholarships
            query={query}
            setQuery={setQuery}
            profileChips={profileChips}
            grouped={grouped}
            onSearch={runSearch}
            onOpen={openScholarship}
            onSave={saveCurrentResult}
            onProfile={() => setScreen("profile")}
          />
        )}

        {screen === "checker" && (
          <ScholarshipDetails
            result={selected}
            profile={savedProfile}
            evidence={evidence}
            auditLog={auditLog}
            onSave={saveCurrentResult}
            onDraft={openDraft}
            onBack={() => setScreen("find")}
            onProfile={() => setScreen("profile")}
          />
        )}

        {screen === "saved" && (
          <SavedResults
            savedResults={savedResults}
            results={results}
            onOpen={(saved) => {
              const result = results.find((item) => item.verification?.id === saved.verification_id);
              if (result) void openScholarship(result);
            }}
            onRemove={removeSavedResult}
          />
        )}
      </main>
    </div>
  );
}

function Sidebar({
  active,
  onNavigate
}: {
  active: Screen;
  onNavigate: (screen: Screen) => void;
}) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <LogoMark />
        <strong>FundMyDegree</strong>
      </div>

      <nav className="nav-list">
        {navItems.map((item) => (
          <button
            className={`nav-item ${active === item.id ? "active" : ""}`}
            key={item.id}
            onClick={() => onNavigate(item.id)}
            type="button"
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}

function Hero({ screen, onBack }: { screen: Screen; onBack: () => void }) {
  const content = {
    profile: {
      title: "Find scholarships that actually fit you.",
      subtitle:
        "Tell us about your study goals and funding needs. We'll do the hard work to match you with opportunities worth your time."
    },
    find: {
      title: "Your scholarship matches",
      subtitle:
        "These scholarships look like a good fit based on your profile. Open them to learn more and see if they're worth your time."
    },
    checker: {
      title: "Does this scholarship fit you?",
      subtitle: "We checked the details against your profile. Here's what we found."
    },
    saved: {
      title: "Saved scholarships",
      subtitle: "Keep track of scholarships you may want to come back to later."
    }
  }[screen];

  return (
    <header className="hero">
      <div className="hero-copy">
        {screen === "checker" && (
          <button className="back-link" onClick={onBack} type="button">
            <ArrowLeft size={18} />
            Back to matches
          </button>
        )}
        <h1>
          {content.title}
          {screen !== "profile" && <Sparkles className="title-sparkle" size={32} />}
        </h1>
        <p>{content.subtitle}</p>
      </div>
    </header>
  );
}

function ProfileWizard({
  profile,
  onSubmit,
  onField,
  onToggleDocument
}: {
  profile: StudentProfile;
  onSubmit: (event: FormEvent) => void;
  onField: <K extends keyof StudentProfile>(field: K, value: StudentProfile[K]) => void;
  onToggleDocument: (name: string) => void;
}) {
  return (
    <form className="profile-card" onSubmit={onSubmit}>
      <div className="section-heading">
        <h2>Let's start with you</h2>
        <span className="wave">hello</span>
        <p>A few quick details so we can find the best scholarships for you.</p>
      </div>

      <ProfileRow
        icon={<UserRound size={26} />}
        title="About you"
        fields={
          <>
            <FieldControl icon={<MapPin size={20} />} label="Where are you from?">
              <select value={profile.nationality} onChange={(e) => onField("nationality", e.target.value)}>
                <option>Sri Lanka</option>
                <option>India</option>
                <option>Bangladesh</option>
                <option>Nepal</option>
                <option>Pakistan</option>
              </select>
            </FieldControl>
            <FieldControl icon={<MapPin size={20} />} label="Where do you live now?">
              <select value={profile.residence} onChange={(e) => onField("residence", e.target.value)}>
                <option>Sri Lanka</option>
                <option>India</option>
                <option>United Kingdom</option>
                <option>Germany</option>
                <option>Other</option>
              </select>
            </FieldControl>
          </>
        }
      />

      <ProfileRow
        icon={<GraduationCap size={28} />}
        title="Study plans"
        note="Share your goals so we can find the right opportunities."
        fields={
          <>
            <FieldControl icon={<GraduationCap size={20} />} label="Degree level">
              <select value={profile.degree_level} onChange={(e) => onField("degree_level", e.target.value)}>
                <option>Master's</option>
                <option>PhD</option>
                <option>Bachelor's</option>
              </select>
            </FieldControl>
            <FieldControl icon={<BookOpen size={20} />} label="What do you want to study?">
              <select value={profile.field} onChange={(e) => onField("field", e.target.value)}>
                <option>Artificial Intelligence</option>
                <option>Computer Science</option>
                <option>Data Science</option>
                <option>Engineering</option>
                <option>Business</option>
              </select>
            </FieldControl>
            <FieldControl icon={<Globe2 size={20} />} label="Where do you want to study?">
              <select
                value={profile.target_regions[0] ?? "Europe"}
                onChange={(e) => onField("target_regions", [e.target.value])}
              >
                <option>Europe</option>
                <option>United Kingdom</option>
                <option>Germany</option>
                <option>Finland</option>
                <option>Sweden</option>
              </select>
            </FieldControl>
            <FieldControl icon={<CalendarDays size={20} />} label="When do you want to start?">
              <select value={profile.intake} onChange={(e) => onField("intake", e.target.value)}>
                <option>2026/27</option>
                <option>2027/28</option>
                <option>As soon as possible</option>
              </select>
            </FieldControl>
            <FieldControl icon={<WalletCards size={20} />} label="How much funding do you need?">
              <select
                value={String(profile.funding_need_percent)}
                onChange={(e) => onField("funding_need_percent", Number(e.target.value))}
              >
                <option value="25">25%+</option>
                <option value="40">40%+</option>
                <option value="50">50%+</option>
                <option value="100">Full funding</option>
              </select>
            </FieldControl>
          </>
        }
      />

      <ProfileRow
        icon={<BriefcaseBusiness size={26} />}
        title="Background"
        note="Help us understand your experience."
        fields={
          <>
            <FieldControl icon={<BarChart3 size={20} />} label="Academic profile">
              <select value={profile.academic_level} onChange={(e) => onField("academic_level", e.target.value)}>
                <option>upper second equivalent</option>
                <option>first class equivalent</option>
                <option>good academic standing</option>
                <option>still studying</option>
              </select>
            </FieldControl>
            <FieldControl icon={<BriefcaseBusiness size={20} />} label="Work experience">
              <select
                value={String(profile.work_experience_years)}
                onChange={(e) => onField("work_experience_years", Number(e.target.value))}
              >
                <option value="0">No work experience</option>
                <option value="1">1 year</option>
                <option value="2">2 years</option>
                <option value="3">3+ years</option>
              </select>
            </FieldControl>
          </>
        }
      />

      <ProfileRow
        icon={<FileText size={26} />}
        title="Documents you already have"
        note="This is only a checklist. Please don't upload private documents here."
        fields={
          <div className="document-grid">
            {documentOptions.map(([value, label]) => (
              <label className="document-chip" key={value}>
                <input
                  checked={profile.documents_available.includes(value)}
                  type="checkbox"
                  onChange={() => onToggleDocument(value)}
                />
                <span>{label}</span>
              </label>
            ))}
          </div>
        }
      />

      <div className="profile-actions">
        <button className="primary-button jumbo-button" type="submit">
          <Sparkles size={20} />
          See my matches
        </button>
        <p>
          <LockKeyhole size={16} />
          Your information is safe and secure.
        </p>
      </div>
    </form>
  );
}

function ProfileRow({
  icon,
  title,
  note,
  fields
}: {
  icon: JSX.Element;
  title: string;
  note?: string;
  fields: ReactNode;
}) {
  return (
    <section className="profile-row">
      <div className="row-label">
        <span className="row-icon">{icon}</span>
        <div>
          <h3>{title}</h3>
          {note && <p>{note}</p>}
        </div>
      </div>
      <div className="row-fields">{fields}</div>
    </section>
  );
}

function FieldControl({
  label,
  icon,
  children
}: {
  label: string;
  icon: JSX.Element;
  children: ReactNode;
}) {
  return (
    <label className="field-control">
      <span>{label}</span>
      <div className="control-shell">
        {icon}
        {children}
        <ChevronDown className="control-chevron" size={18} />
      </div>
    </label>
  );
}

function FindScholarships({
  query,
  setQuery,
  profileChips,
  grouped,
  onSearch,
  onOpen,
  onSave,
  onProfile
}: {
  query: string;
  setQuery: (value: string) => void;
  profileChips: string[][];
  grouped: Record<VerdictStatus, CandidateResult[]>;
  onSearch: () => void;
  onOpen: (result: CandidateResult) => void;
  onSave: (result: CandidateResult) => void;
  onProfile: () => void;
}) {
  const [openSections, setOpenSections] = useState<Record<VerdictStatus, boolean>>({
    eligible: true,
    unclear: false,
    not_eligible: false,
    unverified: false
  });

  return (
    <section className="matches-layout">
      <div className="matches-main">
        <div className="search-card">
          <div className="search-row">
            <div className="search-box">
              <Search size={22} />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search scholarships by name, provider or keyword"
              />
            </div>
            <button className="primary-button" onClick={onSearch} type="button">
              <Sparkles size={20} />
              Find matches
            </button>
          </div>
          <div className="match-chips">
            {profileChips.length ? (
              profileChips.map(([label, value]) => <ProfileChip key={label} label={label} value={value} />)
            ) : (
              <button className="text-button" onClick={onProfile} type="button">
                <Pencil size={18} />
                Start with profile
              </button>
            )}
            <button className="text-button edit-profile" onClick={onProfile} type="button">
              <Pencil size={18} />
              Edit profile
            </button>
          </div>
        </div>

        {(["eligible", "unclear", "not_eligible", "unverified"] as VerdictStatus[]).map((status) => (
          <ResultSection
            isOpen={openSections[status]}
            key={status}
            results={grouped[status]}
            status={status}
            onOpen={onOpen}
            onSave={onSave}
            onToggle={() => setOpenSections((current) => ({ ...current, [status]: !current[status] }))}
          />
        ))}
      </div>

      <aside className="summary-card">
        <h2>Match Summary</h2>
        <Metric icon={<Star size={20} />} label="Best Matches" value={grouped.eligible.length} />
        <Metric icon={<CircleHelp size={20} />} label="Need to Confirm" value={grouped.unclear.length} />
        <Metric icon={<XCircle size={20} />} label="Not for You" value={grouped.not_eligible.length} />
        <Metric icon={<Search size={20} />} label="Couldn't Verify Yet" value={grouped.unverified.length} />
        <div className="summary-note">
          <Sparkles size={20} />
          We use trusted sources and your profile to find the best opportunities for you.
        </div>
      </aside>
    </section>
  );
}

function ProfileChip({ label, value }: { label: string; value: string }) {
  const icon = {
    From: <MapPin size={18} />,
    Degree: <GraduationCap size={18} />,
    Subject: <BookOpen size={18} />,
    Funding: <WalletCards size={18} />,
    Region: <Globe2 size={18} />
  }[label] ?? <Sparkles size={18} />;

  return (
    <span className="profile-chip">
      {icon}
      {label === "Funding" ? `Funding ${value}` : value}
    </span>
  );
}

function ResultSection({
  status,
  results,
  isOpen,
  onToggle,
  onOpen,
  onSave
}: {
  status: VerdictStatus;
  results: CandidateResult[];
  isOpen: boolean;
  onToggle: () => void;
  onOpen: (result: CandidateResult) => void;
  onSave: (result: CandidateResult) => void;
}) {
  const meta = statusMeta[status];
  return (
    <section className={`match-section ${isOpen ? "open" : ""}`}>
      <button className="match-section-header" onClick={onToggle} type="button">
        <span className={`section-icon ${meta.className}`}>{meta.icon}</span>
        <strong>{meta.section}</strong>
        <span className="count-pill">{results.length}</span>
        <ChevronDown className="section-chevron" size={24} />
      </button>
      {isOpen && (
        <div className="match-card-list">
          {results.length === 0 ? (
            <p className="empty-text">No scholarships in this group yet.</p>
          ) : (
            results.map((result) => (
              <ScholarshipCard key={result.candidate.id} result={result} onOpen={onOpen} onSave={onSave} />
            ))
          )}
        </div>
      )}
    </section>
  );
}

function ScholarshipCard({
  result,
  onOpen,
  onSave
}: {
  result: CandidateResult;
  onOpen: (result: CandidateResult) => void;
  onSave: (result: CandidateResult) => void;
}) {
  const { candidate, verification } = result;
  return (
    <article className="scholarship-card">
      <div className="provider-avatar">{providerInitials(candidate.provider)}</div>
      <div className="scholarship-info">
        <div className="card-topline">
          <h3>{candidate.name}</h3>
          <div className="badge-row">
            <StatusBadge status={verification?.status ?? "unverified"} />
            <span className={`source-pill ${verification?.source_official ? "source-official" : ""}`}>
              <ShieldCheck size={16} />
              {verification?.source_official ? "Trusted source" : "Needs source"}
            </span>
          </div>
        </div>
        <p className="provider-line">
          <Globe2 size={18} />
          {candidate.country}
          <span>•</span>
          <Landmark size={18} />
          {candidate.provider}
        </p>
        <p className="funding-line">{fundingLabel(candidate, verification)}</p>
        <div className="scholarship-meta">
          <span>
            <CalendarDays size={23} />
            <strong>Deadline</strong>
            {deadlineLabel(candidate, verification)}
          </span>
          <span>
            <ClockIcon />
            <strong>Intake</strong>
            2026/27
          </span>
        </div>
      </div>
      <div className="card-actions">
        <button className="primary-button" type="button" onClick={() => onOpen(result)}>
          Open match
          <ExternalLink size={20} />
        </button>
        <button className="outline-button" type="button" onClick={() => onSave(result)} disabled={!verification}>
          <Heart size={22} />
          Save
        </button>
      </div>
    </article>
  );
}

function ScholarshipDetails({
  result,
  profile,
  evidence,
  auditLog,
  onSave,
  onDraft,
  onBack,
  onProfile
}: {
  result: CandidateResult | null;
  profile: StudentProfile | null;
  evidence: Evidence | null;
  auditLog: AuditEvent[];
  onSave: (result: CandidateResult) => void;
  onDraft: (result: CandidateResult) => void;
  onBack: () => void;
  onProfile: () => void;
}) {
  if (!result?.verification) {
    return (
      <EmptyPanel
        title="No scholarship selected yet"
        body="Go back to matches and open a scholarship to see whether it may fit you."
        actionLabel="Back to matches"
        onAction={onBack}
      />
    );
  }

  const { candidate, verification } = result;
  const sourceUrl = evidence?.source.url || verification.source_url;
  const checkedAt = formatDate(verification.last_checked);
  const helpfulRisks = verification.blocking_rules.length
    ? verification.blocking_rules
    : [
        quickRule("Competition", "High competition for AI-related programs."),
        quickRule("Motivation", "Strong motivation and clear research goals matter."),
        quickRule("Timing", "Late or incomplete applications are not considered."),
        quickRule("Costs", "Scholarship may not cover all living costs.")
      ];

  return (
    <section className="details-stack">
      <div className="details-hero-card">
        <div className="provider-avatar large">{providerInitials(candidate.provider)}</div>
        <div className="detail-scholarship">
          <h2>{candidate.name}</h2>
          <p>
            <MapPin size={18} />
            {candidate.country}
            <span>•</span>
            <Landmark size={18} />
            {candidate.provider}
          </p>
          <p className="funding-line">{fundingLabel(candidate, verification)}</p>
          <div className="detail-stats">
            <span>
              <WalletCards size={28} />
              <strong>Funding need</strong>
              {profile?.funding_need_percent ?? 0}%
            </span>
            <span>
              <CalendarDays size={28} />
              <strong>Intake</strong>
              {profile?.intake ?? "2026/27"}
            </span>
            <span>
              <ClockIcon />
              <strong>Deadline</strong>
              {deadlineLabel(candidate, verification)}
            </span>
          </div>
        </div>

        <div className="profile-glance">
          <div className="glance-heading">
            <h3>Your profile at a glance</h3>
            <button className="text-button" type="button" onClick={onProfile}>
              <Pencil size={18} />
              Edit profile
            </button>
          </div>
          <div className="glance-grid">
            <MiniFact icon={<Globe2 size={20} />} label="Residence" value={profile?.residence ?? ""} />
            <MiniFact icon={<WalletCards size={20} />} label="Fee status" value={profile?.fee_status ?? ""} />
            <MiniFact icon={<BookOpen size={20} />} label="Field" value={profile?.field ?? ""} />
            <MiniFact icon={<GraduationCap size={20} />} label="Degree level" value={profile?.degree_level ?? ""} />
            <MiniFact
              icon={<BriefcaseBusiness size={20} />}
              label="Work experience"
              value={`${profile?.work_experience_years ?? 0} year`}
            />
            <MiniFact icon={<Landmark size={20} />} label="University preference" value={profile ? displayRegion(profile.target_regions) : ""} />
          </div>
        </div>
      </div>

      <div className="detail-card-grid">
        <CriteriaCard
          tone="match"
          icon={<Star size={28} />}
          title="What matches your profile"
          rules={verification.matched_rules.length ? verification.matched_rules : [quickRule("Profile", "Your profile matches the scholarship basics.")]}
          cta="See all matching criteria"
        />
        <CriteriaCard
          tone="confirm"
          icon={<Search size={28} />}
          title="What we still need to confirm"
          rules={[
            ...verification.unclear_rules,
            ...verification.missing_required_rules.map((rule) => quickRule(rule, `We need clearer evidence for ${friendlyRuleLabel(rule).toLowerCase()}.`))
          ]}
          emptyText="No unclear rules found for this scholarship."
          cta="See details"
        />
        <CriteriaCard
          tone="risk"
          icon={<ShieldCheck size={28} />}
          title="What may affect your application"
          rules={helpfulRisks}
          cta="How to strengthen your application"
        />
      </div>

      <div className="evidence-strip">
        <div>
          <span className="strip-icon">
            <FileText size={30} />
          </span>
          <div>
            <h3>Where this information came from</h3>
            <p>{evidence?.source.reason || verification.source_reason}</p>
            {sourceUrl && (
              <a href={sourceUrl} target="_blank" rel="noreferrer">
                View official scholarship page <ExternalLink size={16} />
              </a>
            )}
          </div>
        </div>
        <div>
          <span className="strip-icon">
            <ShieldCheck size={30} />
          </span>
          <div>
            <h3>How we checked this</h3>
            <p>We compared the scholarship requirements with your profile details.</p>
            <p className="last-checked">Last checked: {checkedAt}</p>
          </div>
          <span className="auto-pill">
            <CheckCircle2 size={18} />
            Auto-checked
          </span>
        </div>
      </div>

      <div className="detail-actions">
        <button className="primary-button jumbo-button" type="button" onClick={() => onSave(result)}>
          <Heart size={24} />
          Save scholarship
        </button>
        <button className="outline-button jumbo-button" type="button" onClick={onBack}>
          <ArrowLeft size={22} />
          Back to matches
        </button>
        <button
          className="soft-button jumbo-button"
          disabled={verification.status !== "unclear"}
          type="button"
          onClick={() => onDraft(result)}
        >
          <UserRound size={22} />
          Ask to confirm
          <CircleHelp size={18} />
        </button>
      </div>
      <p className="secure-note">
        <LockKeyhole size={16} />
        Your information is safe and secure.
      </p>
      {auditLog.length > 0 && <span className="audit-count">{auditLog.length} checks completed</span>}
    </section>
  );
}

function CriteriaCard({
  tone,
  icon,
  title,
  rules,
  cta,
  emptyText
}: {
  tone: "match" | "confirm" | "risk";
  icon: JSX.Element;
  title: string;
  rules: Rule[];
  cta: string;
  emptyText?: string;
}) {
  return (
    <article className={`criteria-card ${tone}`}>
      <div className="criteria-title">
        <span>{icon}</span>
        <h3>{title}</h3>
      </div>
      <ul>
        {rules.length ? (
          rules.slice(0, 5).map((rule) => (
            <li key={`${rule.rule_type}-${rule.requirement_text}`}>
              {tone === "match" ? <CheckCircle2 size={18} /> : tone === "confirm" ? <CircleHelp size={18} /> : <ShieldCheck size={18} />}
              <span>{friendlyRuleSentence(rule)}</span>
            </li>
          ))
        ) : (
          <li className="muted-list-item">
            <CircleHelp size={18} />
            <span>{emptyText ?? "No details in this group."}</span>
          </li>
        )}
      </ul>
      <button className="card-link" type="button">
        {cta}
        <ChevronDown size={18} />
      </button>
    </article>
  );
}

function MiniFact({ icon, label, value }: { icon: JSX.Element; label: string; value: string }) {
  return (
    <span className="mini-fact">
      {icon}
      <strong>{label}</strong>
      {value || "Not set"}
    </span>
  );
}

function SavedResults({
  savedResults,
  results,
  onOpen,
  onRemove
}: {
  savedResults: SavedResult[];
  results: CandidateResult[];
  onOpen: (saved: SavedResult) => void;
  onRemove: (savedId: string) => void;
}) {
  const candidateById = new Map(results.map((item) => [item.candidate.id, item.candidate]));
  return (
    <section className="saved-panel">
      {savedResults.length === 0 ? (
        <EmptyPanel
          title="No saved scholarships yet"
          body="Save scholarships from your matches when you want to come back to them."
        />
      ) : (
        <div className="saved-list">
          {savedResults.map((saved) => {
            const candidate = candidateById.get(saved.candidate_id);
            return (
              <article className="saved-card" key={saved.id}>
                <div className="provider-avatar">{providerInitials(candidate?.provider ?? saved.candidate_id)}</div>
                <div>
                  <StatusBadge status={saved.status} />
                  <h3>{candidate?.name ?? saved.candidate_id}</h3>
                  <p>{candidate?.country ?? "Saved scholarship"} • {candidate?.provider ?? saved.student_facing_status}</p>
                </div>
                <div className="saved-actions">
                  <button className="primary-button" type="button" onClick={() => onOpen(saved)}>
                    View details
                  </button>
                  <button className="outline-button" type="button" onClick={() => onRemove(saved.id)}>
                    Remove
                  </button>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}

function StatusBadge({ status }: { status: VerdictStatus }) {
  const meta = statusMeta[status];
  return (
    <span className={`status-badge ${meta.className}`}>
      {meta.icon}
      {meta.label}
    </span>
  );
}

function Metric({ icon, label, value }: { icon: JSX.Element; label: string; value: number }) {
  return (
    <div className="metric">
      <span>
        {icon}
        {label}
      </span>
      <strong>{value}</strong>
    </div>
  );
}

function EmptyPanel({
  title,
  body,
  actionLabel,
  onAction
}: {
  title: string;
  body: string;
  actionLabel?: string;
  onAction?: () => void;
}) {
  return (
    <section className="empty-panel">
      <h2>{title}</h2>
      <p>{body}</p>
      {actionLabel && onAction && (
        <button className="primary-button" type="button" onClick={onAction}>
          {actionLabel}
        </button>
      )}
    </section>
  );
}

function LogoMark() {
  return (
    <span className="logo-mark">
      <GraduationCap size={22} />
      <span />
    </span>
  );
}

function ClockIcon() {
  return (
    <span className="clock-icon" aria-hidden="true">
      <span />
    </span>
  );
}

function providerInitials(value: string) {
  const compact = value.replace(/University of /i, "").replace(/Study in /i, "");
  if (/daad/i.test(value)) return "DAAD";
  return compact
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0]?.toUpperCase())
    .join("");
}

function compareDemoResults(a: CandidateResult, b: CandidateResult) {
  const statusRank: Record<VerdictStatus, number> = {
    eligible: 0,
    unclear: 1,
    not_eligible: 2,
    unverified: 3
  };
  const aStatus = statusRank[a.verification?.status ?? "unverified"];
  const bStatus = statusRank[b.verification?.status ?? "unverified"];
  if (aStatus !== bStatus) return aStatus - bStatus;
  const aDaad = /daad/i.test(a.candidate.provider) ? 0 : 1;
  const bDaad = /daad/i.test(b.candidate.provider) ? 0 : 1;
  if (aDaad !== bDaad) return aDaad - bDaad;
  return a.candidate.name.localeCompare(b.candidate.name);
}

function displayRegion(regions: string[]) {
  if (regions.includes("Europe")) return "Europe";
  return regions.join(", ");
}

function quickRule(ruleType: string, text: string): Rule {
  return {
    rule_type: ruleType,
    requirement_text: text,
    evidence_text: text,
    status: "unclear",
    source_url: "",
    confidence: 0.5
  };
}

function friendlyRuleSentence(rule: Rule) {
  if (rule.evidence_text) return rule.evidence_text;
  if (rule.requirement_text) return rule.requirement_text;
  return friendlyRuleLabel(rule.rule_type);
}

function friendlyRuleLabel(value: string) {
  return (
    {
      current_cycle: "Study year",
      nationality: "Country eligibility",
      residence: "Where you live",
      fee_status: "Fee category",
      degree_level: "Degree level",
      field: "Subject area",
      funding_amount: "Funding",
      deadline: "Deadline",
      application_process: "How to apply"
    }[value] ?? value.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase())
  );
}

function formatDate(value?: string) {
  if (!value) return "Not checked";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function fundingFromVerification(verification?: Verification) {
  const rule = verification?.matched_rules.find((item) => item.rule_type === "funding_amount");
  return rule?.evidence_text || "See funding details";
}

function deadlineFromVerification(verification?: Verification) {
  const rule = verification?.matched_rules.find((item) => item.rule_type === "deadline");
  return rule?.evidence_text || "See details";
}

function fundingLabel(candidate: ScholarshipCandidate, verification?: Verification) {
  const value = candidate.funding_text || fundingFromVerification(verification);
  return value
    .replace(/^Official\s+\w+\s+page\s+(lists|states|says)\s+/i, "")
    .replace(/^Official page\s+(lists|states|says)\s+/i, "")
    .replace(/\band monthly\b/i, "+ monthly")
    .replace(/\.$/, ".");
}

function deadlineLabel(candidate: ScholarshipCandidate, verification?: Verification) {
  const value = candidate.deadline_text || deadlineFromVerification(verification);
  const match = value.match(/\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b/i);
  if (!match) return value.length > 34 ? "See official page" : value;

  const month = {
    january: "Jan",
    february: "Feb",
    march: "Mar",
    april: "Apr",
    may: "May",
    june: "Jun",
    july: "Jul",
    august: "Aug",
    september: "Sep",
    october: "Oct",
    november: "Nov",
    december: "Dec"
  }[match[2].toLowerCase()];
  return `${match[1]} ${month} ${match[3]}`;
}

export default App;
