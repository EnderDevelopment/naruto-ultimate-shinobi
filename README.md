# Minecraft Bedrock Naruto Add-On

Naruto Ultimate Shinobi is a Minecraft Bedrock mod add-on that adds Naruto Uzumaki as the first playable shinobi stage, with a custom 3D model, 128x128 texture, idle and running animations, Naruto AI, melee combat, Rasengan, Shadow Clone Scroll, Headband activation, enhanced movement, and water-running behavior for Android-compatible Bedrock worlds.

## Install

1. Install Minecraft Bedrock Edition 1.21.0 or newer.
2. Install Python 3 and the `zip` utility on a computer.
3. Run the texture and packaging script from the project directory:

   ```sh
   sh package-addon.sh
   ```

4. The script validates the Behavior Pack and Resource Pack JSON files, generates the texture assets, and creates:

   ```text
   build/naruto-ultimate-shinobi-naruto.mcaddon
   ```

5. Transfer the `.mcaddon` file to an Android device with Minecraft Bedrock installed.
6. Open the file with Minecraft and import both packs.
7. Create or open a test world.
8. Activate the Behavior Pack and Resource Pack for the world.
9. Enable the Script API or Beta APIs required by the installed Minecraft Bedrock version.

## Use

Use the following commands in the world:

```text
/give @s nus:naruto_headband
/give @s nus:rasengan
/give @s nus:shadow_clone_scroll
/summon nus:naruto
```

Use the Naruto Headband to activate or deactivate Naruto mode.

When Naruto mode is active, the player receives:

- Increased movement speed through a Speed effect.
- Approximately triple jump height through a Jump Boost effect.
- Water-running behavior that moves the player onto the water surface when suitable conditions are detected.

Use the Rasengan to damage nearby non-player entities within approximately four blocks. The ability applies damage, knockback, a particle effect, and an item cooldown.

Use the Shadow Clone Scroll to summon three temporary Naruto entities around the player. The clones disappear after approximately ten seconds.

The summoned Naruto entity has custom geometry and texture assets, idle and running animations, wandering behavior, monster targeting, melee attacks, health, collision, water pathing, and a Naruto Headband loot drop.

The add-on source contains the following packs:

- `behavior_pack`: entity behavior, items, loot table, scripts, and manifests.
- `resource_pack`: entity model, texture, animations, render controller, item icons, and manifests.

Runtime testing must be completed in Minecraft Bedrock on Android. The workspace can validate JSON files and create the `.mcaddon`, but it cannot launch Minecraft or verify exact movement multipliers on a device.

---

More Minecraft mod projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/188fb8a5-dccf-4f0c-abcc-068de43b7b5c?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=188fb8a5-dccf-4f0c-abcc-068de43b7b5c
