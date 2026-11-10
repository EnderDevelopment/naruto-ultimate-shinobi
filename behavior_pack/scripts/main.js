import { world, system, EntityDamageCause } from "@minecraft/server";

const activeNaruto = new Set();
const cloneExpiry = new Map();
const ITEM_HEADBAND = "nus:naruto_headband";
const ITEM_RASENGAN = "nus:rasengan";
const ITEM_CLONE = "nus:shadow_clone_scroll";

world.afterEvents.itemUse.subscribe((event) => {
  const player = event.source;
  if (player.typeId !== "minecraft:player") return;
  if (event.itemStack.typeId === ITEM_HEADBAND) {
    if (activeNaruto.has(player.id)) {
      activeNaruto.delete(player.id);
      player.sendMessage("Naruto mode deactivated.");
    } else {
      activeNaruto.add(player.id);
      player.sendMessage("Naruto mode activated: enhanced speed, triple jump, and water running enabled.");
    }
    return;
  }
  if (event.itemStack.typeId === ITEM_RASENGAN) {
    useRasengan(player);
    return;
  }
  if (event.itemStack.typeId === ITEM_CLONE) summonClones(player);
});

function useRasengan(player) {
  const dimension = player.dimension;
  const origin = player.location;
  dimension.spawnParticle("minecraft:blue_flame_particle", { x: origin.x, y: origin.y + 1, z: origin.z });
  for (const target of dimension.getEntities({ location: origin, maxDistance: 4 })) {
    if (target.id === player.id || target.typeId === "minecraft:player" || target.typeId === "nus:naruto") continue;
    try {
      target.applyDamage(18, { cause: EntityDamageCause.entityAttack, damagingEntity: player });
      const dx = target.location.x - origin.x;
      const dz = target.location.z - origin.z;
      const length = Math.max(0.1, Math.hypot(dx, dz));
      target.applyImpulse({ x: (dx / length) * 1.1, y: 0.55, z: (dz / length) * 1.1 });
    } catch {
      // Some entities do not accept damage or knockback.
    }
  }
  player.sendMessage("Rasengan!");
}

function summonClones(player) {
  const dimension = player.dimension;
  const base = player.location;
  for (let index = 0; index < 3; index++) {
    const angle = (Math.PI * 2 * index) / 3;
    const clone = dimension.spawnEntity("nus:naruto", { x: base.x + Math.cos(angle) * 2, y: base.y, z: base.z + Math.sin(angle) * 2 });
    clone.nameTag = "Shadow Clone";
    cloneExpiry.set(clone.id, system.currentTick + 200);
  }
  dimension.spawnParticle("minecraft:basic_smoke_particle", { x: base.x, y: base.y + 1, z: base.z });
}

function isWater(block) {
  return !!block && (block.typeId === "minecraft:water" || block.typeId === "minecraft:flowing_water");
}

system.runInterval(() => {
  for (const player of world.getAllPlayers()) {
    if (!activeNaruto.has(player.id)) continue;
    try {
      player.addEffect("speed", 30, { amplifier: 19, showParticles: false });
      player.addEffect("jump_boost", 30, { amplifier: 2, showParticles: false });
      const pos = player.location;
      const blockX = Math.floor(pos.x);
      const blockZ = Math.floor(pos.z);
      const waterY = Math.floor(pos.y - 0.05);
      const water = player.dimension.getBlock({ x: blockX, y: waterY, z: blockZ });
      const headSpace = player.dimension.getBlock({ x: blockX, y: waterY + 2, z: blockZ });
      if (isWater(water) && headSpace && headSpace.typeId === "minecraft:air" && pos.y < waterY + 1.25) {
        player.teleport({ x: pos.x, y: waterY + 1.02, z: pos.z }, { dimension: player.dimension, checkForBlocks: false });
      }
    } catch {
      activeNaruto.delete(player.id);
    }
  }
  for (const dimensionId of ["overworld", "nether", "the_end"]) {
    const dimension = world.getDimension(dimensionId);
    for (const entity of dimension.getEntities({ type: "nus:naruto" })) {
      const expiry = cloneExpiry.get(entity.id);
      if (expiry !== undefined && system.currentTick >= expiry) {
        try { entity.remove(); } catch {}
        cloneExpiry.delete(entity.id);
      }
    }
  }
}, 5);

world.afterEvents.playerLeave.subscribe((event) => activeNaruto.delete(event.playerId));
