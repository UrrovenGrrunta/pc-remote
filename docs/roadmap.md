# PC Remote Roadmap

This roadmap defines the work required to move PC Remote from **Active** to **Finished**.

The project is considered finished when its core remote-control workflow is reliable for normal personal use. Experimental integrations do not need to block the first finished version.

## 1. Core remote control — mostly done

- [x] Run a lightweight HTTP server on the Windows PC.
- [x] Access the interface remotely through Tailscale.
- [x] Serve a mobile-friendly web interface.
- [x] Discover installed Steam games from `appmanifest_*.acf` files.
- [x] Load Steam game metadata and artwork.
- [x] Build game cards dynamically in the frontend.
- [x] Launch Steam games by AppID.
- [x] Launch configured non-Steam applications.
- [x] Support custom launch actions such as osu! + OpenTabletDriver and Guitar Rig 7.
- [x] Provide the restart-into-Ubuntu workflow.

## 2. Configuration and setup — in progress

- [x] Move machine-specific configuration into `config.json`.
- [x] Add project path handling.
- [x] Add initial setup-related code.
- [ ] Review the current setup flow and remove any remaining unnecessary hard-coded machine-specific values.
- [ ] Make first-time setup clear enough that reinstalling PC Remote on the same PC does not require editing source code.
- [ ] Verify that missing or invalid configuration fails with a useful error instead of an obscure traceback.

## 3. Game and application sources

### Steam

- [x] Discover installed games.
- [x] Retrieve metadata.
- [x] Launch games.
- [ ] Verify behaviour when Steam metadata or artwork cannot be retrieved.

### Standalone applications

- [x] Support standalone application definitions.
- [x] Support standalone presets/custom launch behaviour.
- [ ] Verify configured standalone applications with the current setup/configuration flow.

### Hydra

- [x] Investigate Hydra's local library storage.
- [x] Attempt direct LevelDB/SSTable parsing.
- [x] Preserve failed/legacy approaches in the project history where useful.
- [ ] Decide whether Hydra support is viable enough for the finished version.

Hydra is **not required** for PC Remote to become Finished. If reliable integration remains disproportionately difficult, the experimental provider can stay experimental or be frozen without blocking completion.

## 4. Reliability pass

- [ ] Test the normal phone → Tailscale → PC workflow end to end.
- [ ] Test launching several Steam games.
- [ ] Test configured standalone applications.
- [ ] Test custom launch actions.
- [ ] Test the Ubuntu restart action.
- [ ] Check behaviour for unavailable games/apps and malformed requests.
- [ ] Remove or resolve obviously dead temporary code such as empty test/placeholder files where appropriate.

The goal here is not exhaustive enterprise-grade testing. PC Remote is a personal tool; the important requirement is that the workflows actually used on the target PC are dependable.

## 5. Finish pass

- [ ] Update README so it accurately describes the final supported feature set.
- [ ] Document the final setup/configuration procedure.
- [ ] Clearly label any remaining experimental functionality.
- [ ] Perform a clean-install/startup check.
- [ ] Change `Project status: Active` to `Project status: Finished`.

## Definition of Done

PC Remote can be marked **Finished** when:

1. it can be installed/configured on the target Windows PC without modifying application source code;
2. the web interface is reliably reachable from the phone through Tailscale;
3. Steam and configured standalone applications can be launched reliably;
4. the custom actions actually used by the project work;
5. failures in normal usage do not crash the application without a useful explanation;
6. the README contains enough information to set the project up again later.

Hydra support is optional for this milestone. New integrations and convenience features can be added after the project reaches Finished status.