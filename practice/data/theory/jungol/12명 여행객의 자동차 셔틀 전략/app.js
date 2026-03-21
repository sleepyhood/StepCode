const scenario = {
  totalKm: 20,
  totalHours: 2.6,
  rideHours: 0.6,
  walkHours: 2,
  steps: [
    {
      title: "출발 준비",
      timeHours: 0,
      summary:
        "12명을 4명씩 A조, B조, C조로 나눕니다. 세 조가 공평하게 차 36분, 걷기 2시간을 가져야 마지막에 동시에 도착합니다.",
      car: { fromKm: 0, toKm: 0, mode: "wait", label: "출발선에서 대기" },
      groups: {
        A: { km: 0, state: "차를 탈 준비", rideMin: 0, walkMin: 0 },
        B: { km: 0, state: "출발 대기", rideMin: 0, walkMin: 0 },
        C: { km: 0, state: "출발 대기", rideMin: 0, walkMin: 0 },
      },
    },
    {
      title: "1단계: A조가 먼저 36분 탑승",
      timeHours: 0.6,
      summary:
        "차는 A조를 12km 지점까지 데려다줍니다. 같은 36분 동안 B조와 C조는 2.4km씩 걸었습니다.",
      car: { fromKm: 0, toKm: 12, mode: "forward", label: "A조 하차" },
      groups: {
        A: { km: 12, state: "내려서 걷기 시작", rideMin: 36, walkMin: 0 },
        B: { km: 2.4, state: "걷는 중", rideMin: 0, walkMin: 36 },
        C: { km: 2.4, state: "걷는 중", rideMin: 0, walkMin: 36 },
      },
    },
    {
      title: "2단계: 차가 돌아와 B조를 만남",
      timeHours: 1,
      summary:
        "빈 차가 뒤로 달려와 4km 지점에서 B조를 만납니다. A조는 그 사이 13.6km까지 걸었습니다.",
      car: { fromKm: 12, toKm: 4, mode: "backward", label: "B조 승차" },
      groups: {
        A: { km: 13.6, state: "계속 걷는 중", rideMin: 36, walkMin: 24 },
        B: { km: 4, state: "차를 만나 탑승", rideMin: 0, walkMin: 60 },
        C: { km: 4, state: "계속 걷는 중", rideMin: 0, walkMin: 60 },
      },
    },
    {
      title: "3단계: B조도 36분 탑승",
      timeHours: 1.6,
      summary:
        "B조는 36분 동안 차를 타고 16km 지점까지 갑니다. C조는 계속 걸어서 6.4km 지점에 도달합니다.",
      car: { fromKm: 4, toKm: 16, mode: "forward", label: "B조 하차" },
      groups: {
        A: { km: 16, state: "계속 걷는 중", rideMin: 36, walkMin: 60 },
        B: { km: 16, state: "내려서 걷기 시작", rideMin: 36, walkMin: 60 },
        C: { km: 6.4, state: "걷는 중", rideMin: 0, walkMin: 96 },
      },
    },
    {
      title: "4단계: 차가 돌아와 C조를 만남",
      timeHours: 2,
      summary:
        "차는 다시 뒤로 와서 8km 지점에서 C조를 만납니다. 이때 A조와 B조는 이미 17.6km까지 와 있습니다.",
      car: { fromKm: 16, toKm: 8, mode: "backward", label: "C조 승차" },
      groups: {
        A: { km: 17.6, state: "마지막 구간 걷는 중", rideMin: 36, walkMin: 84 },
        B: { km: 17.6, state: "마지막 구간 걷는 중", rideMin: 36, walkMin: 84 },
        C: { km: 8, state: "차를 만나 탑승", rideMin: 0, walkMin: 120 },
      },
    },
    {
      title: "5단계: 모두 동시에 도착",
      timeHours: 2.6,
      summary:
        "C조가 마지막 12km를 차로 가는 36분 동안 A조와 B조는 남은 2.4km를 걷습니다. 세 조 모두 정확히 2시간 36분에 도착합니다.",
      car: { fromKm: 8, toKm: 20, mode: "forward", label: "목적지 도착" },
      groups: {
        A: { km: 20, state: "도착", rideMin: 36, walkMin: 120 },
        B: { km: 20, state: "도착", rideMin: 36, walkMin: 120 },
        C: { km: 20, state: "도착", rideMin: 36, walkMin: 120 },
      },
    },
  ],
};

const roles = [
  { key: "car", label: "자동차", className: "car" },
  { key: "A", label: "A조", className: "a" },
  { key: "B", label: "B조", className: "b" },
  { key: "C", label: "C조", className: "c" },
];

const refs = {
  prevBtn: document.getElementById("prevBtn"),
  playBtn: document.getElementById("playBtn"),
  nextBtn: document.getElementById("nextBtn"),
  stepRange: document.getElementById("stepRange"),
  stageMeta: document.getElementById("stageMeta"),
  ruler: document.getElementById("ruler"),
  trackList: document.getElementById("trackList"),
  currentStepNo: document.getElementById("currentStepNo"),
  currentTitle: document.getElementById("currentTitle"),
  currentTime: document.getElementById("currentTime"),
  currentSummary: document.getElementById("currentSummary"),
  groupGrid: document.getElementById("groupGrid"),
};

let currentStep = 0;
let timerId = 0;

function formatDistance(km) {
  const rounded = Math.round(Number(km || 0) * 10) / 10;
  return Number.isInteger(rounded) ? `${rounded}km` : `${rounded.toFixed(1)}km`;
}

function formatHours(hours) {
  const totalMinutes = Math.round(Number(hours || 0) * 60);
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  if (!h) return `${m}분`;
  if (!m) return `${h}시간`;
  return `${h}시간 ${m}분`;
}

function toPercent(km) {
  const ratio = Math.max(0, Math.min(1, Number(km || 0) / scenario.totalKm));
  return `${ratio * 100}%`;
}

function buildRuler() {
  [0, 5, 10, 15, 20].forEach((km) => {
    const tick = document.createElement("span");
    tick.textContent = `${km}km`;
    tick.style.left = `${(km / scenario.totalKm) * 100}%`;
    refs.ruler.appendChild(tick);
  });
}

function buildTracks() {
  const trackRefs = {};
  roles.forEach((role) => {
    const row = document.createElement("div");
    row.className = "track-row";

    const label = document.createElement("div");
    label.className = "track-label";
    label.textContent = role.label;

    const track = document.createElement("div");
    track.className = `track track--${role.className}`;

    const segment = document.createElement("div");
    segment.className = "segment";

    const marker = document.createElement("div");
    marker.className = "marker";

    const markerPos = document.createElement("span");
    markerPos.className = "marker-pos";

    track.append(segment, marker, markerPos);
    row.append(label, track);
    refs.trackList.appendChild(row);

    trackRefs[role.key] = { segment, marker, markerPos };
  });
  return trackRefs;
}

function buildGroupCards() {
  const groupRefs = {};
  ["A", "B", "C"].forEach((key) => {
    const card = document.createElement("section");
    card.className = `group-card group-card--${key.toLowerCase()}`;

    const title = document.createElement("h4");
    title.textContent = `${key}조`;

    const position = document.createElement("div");
    position.className = "group-line";
    const state = document.createElement("div");
    state.className = "group-line";
    const ride = document.createElement("div");
    ride.className = "group-line";
    const walk = document.createElement("div");
    walk.className = "group-line";

    card.append(title, position, state, ride, walk);
    refs.groupGrid.appendChild(card);
    groupRefs[key] = { position, state, ride, walk };
  });
  return groupRefs;
}

const trackRefs = buildTracks();
const groupRefs = buildGroupCards();
buildRuler();

function stopAutoPlay() {
  if (!timerId) return;
  window.clearInterval(timerId);
  timerId = 0;
  refs.playBtn.textContent = "자동 재생";
}

function renderStep(index) {
  const step = scenario.steps[index];
  if (!step) return;

  currentStep = index;
  refs.stepRange.value = String(index);
  refs.stageMeta.textContent = `단계 ${index + 1} / ${scenario.steps.length}`;
  refs.currentStepNo.textContent = `현재 단계 ${index + 1}`;
  refs.currentTitle.textContent = step.title;
  refs.currentTime.textContent = `지금까지 지난 시간: ${formatHours(step.timeHours)}`;
  refs.currentSummary.textContent = step.summary;

  const carLeft = Math.min(step.car.fromKm, step.car.toKm);
  const carWidth = Math.abs(step.car.toKm - step.car.fromKm);
  trackRefs.car.segment.style.left = toPercent(carLeft);
  trackRefs.car.segment.style.width = toPercent(carWidth);
  trackRefs.car.segment.dataset.mode = step.car.mode;
  trackRefs.car.marker.style.left = toPercent(step.car.toKm);
  trackRefs.car.markerPos.style.left = toPercent(step.car.toKm);
  trackRefs.car.markerPos.textContent = `${step.car.label} · ${formatDistance(step.car.toKm)}`;

  ["A", "B", "C"].forEach((key) => {
    const group = step.groups[key];
    const mode = group.state.includes("걷") ? "walk" : "ride";

    trackRefs[key].segment.style.left = "0%";
    trackRefs[key].segment.style.width = toPercent(group.km);
    trackRefs[key].segment.dataset.mode = mode;
    trackRefs[key].marker.style.left = toPercent(group.km);
    trackRefs[key].markerPos.style.left = toPercent(group.km);
    trackRefs[key].markerPos.textContent = formatDistance(group.km);

    groupRefs[key].position.textContent = `위치: ${formatDistance(group.km)}`;
    groupRefs[key].state.textContent = `상태: ${group.state}`;
    groupRefs[key].ride.textContent = `누적 차 탑승: ${group.rideMin}분`;
    groupRefs[key].walk.textContent = `누적 걷기: ${group.walkMin}분`;
  });

  refs.prevBtn.disabled = index === 0;
  refs.nextBtn.disabled = index === scenario.steps.length - 1;
}

refs.prevBtn.addEventListener("click", () => {
  stopAutoPlay();
  renderStep(Math.max(0, currentStep - 1));
});

refs.nextBtn.addEventListener("click", () => {
  stopAutoPlay();
  renderStep(Math.min(scenario.steps.length - 1, currentStep + 1));
});

refs.stepRange.addEventListener("input", () => {
  stopAutoPlay();
  renderStep(Number(refs.stepRange.value || "0"));
});

refs.playBtn.addEventListener("click", () => {
  if (timerId) {
    stopAutoPlay();
    return;
  }

  if (currentStep >= scenario.steps.length - 1) renderStep(0);
  refs.playBtn.textContent = "정지";
  timerId = window.setInterval(() => {
    if (currentStep >= scenario.steps.length - 1) {
      stopAutoPlay();
      return;
    }
    renderStep(currentStep + 1);
  }, 1700);
});

renderStep(0);
