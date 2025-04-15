class TrafficGenerator(threading.Thread):
    def __init__(self, play_action_screen_instance, update_interval_range=(1, 3), daemon=True):
        super().__init__(daemon=daemon)
        self.play_screen = play_action_screen_instance
        self._running = True
        self.update_interval_range = update_interval_range

    def stop(self):
        self._running = False

    def run(self):
        """Simulate game traffic and update the current game action."""
        counter = 0
        while self._running and self.play_screen.game_time_remaining > 0:
            if len(self.play_screen.red_players) >= 1 and len(self.play_screen.green_players) >= 1:
                red_player = random.choice(self.play_screen.red_players)
                green_player = random.choice(self.play_screen.green_players)

                red_equip_id = red_player[2]
                green_equip_id = green_player[2]

                # Simulate interactions between players
                if random.randint(1, 2) == 1:
                    action_text = f"{red_player[1]} hit {green_player[1]}"
                    equipment_code = f"{red_equip_id}:{green_equip_id}"
                else:
                    action_text = f"{green_player[1]} hit {red_player[1]}"
                    equipment_code = f"{green_equip_id}:{red_equip_id}"

                centered_text = f"<div style='text-align: center;'>{action_text}</div>"

                # Use a signal to safely update the UI from the background thread
                self.play_screen.append_action_signal.emit(centered_text)

                if self.play_screen.photon_network:
                    self.play_screen.photon_network.equipID(equipment_code)  # Broadcast equipment code to server
                else:
                    print(f"Skipping network broadcast: {equipment_code}")

                # Simulate base hits after specific iterations
                if counter == 10:
                    base_hit_text = f"{red_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.play_screen.append_action_signal.emit(centered_base_hit_text)
                    if self.play_screen.photon_network:
                        self.play_screen.photon_network.equipID(f"{red_equip_id}:43")  # Red team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")
                elif counter == 20:
                    base_hit_text = f"{green_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.play_screen.append_action_signal.emit(centered_base_hit_text)
                    if self.play_screen.photon_network:
                        self.play_screen.photon_network.equipID(f"{green_equip_id}:53")  # Green team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")

                counter += 1
                time.sleep(random.randint(*self.update_interval_range))
            else:
                time.sleep(1) # Avoid busy-waiting if no players
        print("Traffic generator stopped.")