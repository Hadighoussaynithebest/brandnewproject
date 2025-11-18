(() => {
  const canvas = document.getElementById('scanCanvas');
  const ctx = canvas.getContext('2d');
  const W = canvas.width = 520;
  const H = canvas.height = 360;

  // Convert CSS pixels to canvas pixels for high-DPI
  const DPR = window.devicePixelRatio || 1;
  if (DPR !== 1) {
    canvas.width = W * DPR;
    canvas.height = H * DPR;
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.scale(DPR, DPR);
  }

  const particles = [];
  const shield = {x: W/2, y: H - 60, r: 48};

  function rand(min,max){return Math.random()*(max-min)+min}

  function spawnVirus(){
    const angle = rand(-Math.PI, Math.PI);
    const edge = Math.random() > 0.5 ? 'left' : 'right';
    const x = edge === 'left' ? -20 : W + 20;
    const y = rand(20, H-120);
    particles.push({x,y,vx:rand(-0.6,0.6),vy:rand(-0.2,0.2),r:rand(4,10),life:0,dead:false});
  }

  function update(dt){
    // random spawn
    if(Math.random() < 0.06) spawnVirus();

    for(let i=particles.length-1;i>=0;i--){
      const p = particles[i];
      // slow drift left/right and downward
      p.x += p.vx + Math.sin(p.life*0.05)*0.2;
      p.y += 0.2 + p.vy;
      p.life += 1;

      // attraction to shield when scan active
      if(window.scanActive){
        const dx = shield.x - p.x;
        const dy = shield.y - p.y;
        const dist = Math.sqrt(dx*dx+dy*dy);
        const strength = Math.max(0, 1 - (dist / 420));
        p.x += dx * 0.02 * strength;
        p.y += dy * 0.02 * strength;
        if(dist < shield.r + 8){
          // extermination effect
          p.dead = true;
          spawnExplosion(p.x,p.y);
        }
      }

      // remove off-canvas
      if(p.x < -40 || p.x > W+40 || p.y > H+40 || p.y < -40 || p.dead){
        particles.splice(i,1);
      }
    }

    // update explosions
    for(let i=explosions.length-1;i>=0;i--){
      const e = explosions[i];
      e.t += dt;
      if(e.t > e.d) explosions.splice(i,1);
    }
  }

  const explosions = [];
  function spawnExplosion(x,y){
    explosions.push({x,y,t:0,d:520});
  }

  function draw(){
    // clear
    ctx.clearRect(0,0,W,H);

    // background grid subtle
    ctx.save();
    ctx.fillStyle = 'rgba(3,6,23,0.4)';
    ctx.fillRect(0,0,W,H);
    ctx.restore();

    // viruses
    for(const p of particles){
      ctx.beginPath();
      ctx.fillStyle = `rgba(255,90,90,0.9)`;
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fill();
      ctx.closePath();
      // little glow
      ctx.beginPath();
      const g = ctx.createRadialGradient(p.x,p.y,p.r*0.2,p.x,p.y,p.r*2);
      g.addColorStop(0,'rgba(255,120,120,0.06)');
      g.addColorStop(1,'rgba(255,120,120,0)');
      ctx.fillStyle = g;
      ctx.arc(p.x,p.y,p.r*2,0,Math.PI*2);
      ctx.fill();
      ctx.closePath();
    }

    // explosions
    for(const e of explosions){
      const progress = e.t / e.d;
      const alpha = (1 - progress);
      ctx.beginPath();
      ctx.strokeStyle = `rgba(180,220,255,${alpha})`;
      ctx.lineWidth = 2 + progress*6;
      ctx.arc(e.x,e.y,progress*40,0,Math.PI*2);
      ctx.stroke();
      ctx.closePath();
    }

    // scanning radial pulse from shield
    if(window.scanActive){
      const t = performance.now()*0.002;
      ctx.beginPath();
      const pulseR = 80 + Math.abs(Math.sin(t))*60;
      ctx.strokeStyle = 'rgba(0,245,255,0.06)';
      ctx.lineWidth = 2;
      ctx.arc(shield.x,shield.y,pulseR,0,Math.PI*2);
      ctx.stroke();
      ctx.closePath();
    }

    // shield outline
    ctx.beginPath();
    const grad = ctx.createLinearGradient(shield.x-shield.r,0,shield.x+shield.r,0);
    grad.addColorStop(0,'rgba(0,245,255,0.14)');
    grad.addColorStop(1,'rgba(124,77,255,0.14)');
    ctx.fillStyle = grad;
    ctx.arc(shield.x,shield.y,shield.r,0,Math.PI*2);
    ctx.fill();
    ctx.closePath();

    // center highlight
    ctx.beginPath();
    ctx.fillStyle = 'rgba(255,255,255,0.06)';
    ctx.arc(shield.x,shield.y,14,0,Math.PI*2);
    ctx.fill();
    ctx.closePath();
  }

  let last = performance.now();
  function loop(now){
    const dt = now - last;
    last = now;
    update(dt);
    draw();
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);

  // The website no longer exposes scan controls — keep the canvas decorative only.
  // Seed some particles for a subtle animated background.
  for(let i=0;i<12;i++) spawnVirus();
  window.scanActive = false;

})();
