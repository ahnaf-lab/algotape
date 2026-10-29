import unittest

from algotape.player import Player, PlayerError, PlayerState


class TestPlayerConstruction(unittest.TestCase):
    def test_starts_paused_at_frame_zero(self):
        player = Player(5)
        self.assertEqual(player.index, 0)
        self.assertFalse(player.playing)

    def test_rejects_non_positive_frame_count(self):
        with self.assertRaises(PlayerError):
            Player(0)
        with self.assertRaises(PlayerError):
            Player(-1)

    def test_single_frame_cassette_is_always_at_start_and_end(self):
        player = Player(1)
        self.assertTrue(player.at_start)
        self.assertTrue(player.at_end)


class TestPlayPause(unittest.TestCase):
    def test_play_sets_playing_true(self):
        player = Player(3)
        player.play()
        self.assertTrue(player.playing)

    def test_pause_sets_playing_false(self):
        player = Player(3)
        player.play()
        player.pause()
        self.assertFalse(player.playing)

    def test_toggle_flips_state(self):
        player = Player(3)
        player.toggle()
        self.assertTrue(player.playing)
        player.toggle()
        self.assertFalse(player.playing)

    def test_play_on_last_frame_is_a_no_op(self):
        player = Player(2)
        player.seek(1)
        player.play()
        self.assertFalse(player.playing)


class TestTick(unittest.TestCase):
    def test_tick_while_paused_does_not_advance(self):
        player = Player(3)
        player.tick()
        self.assertEqual(player.index, 0)

    def test_tick_while_playing_advances_one_frame(self):
        player = Player(3)
        player.play()
        player.tick()
        self.assertEqual(player.index, 1)
        self.assertTrue(player.playing)

    def test_tick_auto_pauses_on_reaching_last_frame(self):
        player = Player(3)
        player.play()
        player.tick()  # 0 -> 1
        player.tick()  # 1 -> 2 (last), auto-pause
        self.assertEqual(player.index, 2)
        self.assertFalse(player.playing)

    def test_tick_past_end_is_a_no_op(self):
        player = Player(2)
        player.play()
        player.tick()
        player.tick()
        player.tick()
        self.assertEqual(player.index, 1)
        self.assertFalse(player.playing)


class TestStepAndRewind(unittest.TestCase):
    def test_step_forward_advances_and_pauses(self):
        player = Player(3)
        player.play()
        player.step_forward()
        self.assertEqual(player.index, 1)
        self.assertFalse(player.playing)

    def test_step_forward_clamps_at_last_frame(self):
        player = Player(3)
        player.seek(2)
        player.step_forward()
        self.assertEqual(player.index, 2)

    def test_step_backward_retreats_and_pauses(self):
        player = Player(3)
        player.seek(2)
        player.play()
        player.step_backward()
        self.assertEqual(player.index, 1)
        self.assertFalse(player.playing)

    def test_step_backward_clamps_at_first_frame(self):
        player = Player(3)
        player.step_backward()
        self.assertEqual(player.index, 0)

    def test_rewind_returns_to_start_and_pauses(self):
        player = Player(5)
        player.seek(4)
        player.play()
        player.rewind()
        self.assertEqual(player.index, 0)
        self.assertFalse(player.playing)


class TestSeek(unittest.TestCase):
    def test_seek_moves_to_requested_index(self):
        player = Player(5)
        player.seek(3)
        self.assertEqual(player.index, 3)

    def test_seek_clamps_above_range(self):
        player = Player(5)
        player.seek(99)
        self.assertEqual(player.index, 4)

    def test_seek_clamps_below_range(self):
        player = Player(5)
        player.seek(-10)
        self.assertEqual(player.index, 0)

    def test_seek_pauses_playback(self):
        player = Player(5)
        player.play()
        player.seek(2)
        self.assertFalse(player.playing)


class TestStartEndFlags(unittest.TestCase):
    def test_at_start_and_at_end_flags(self):
        player = Player(3)
        self.assertTrue(player.at_start)
        self.assertFalse(player.at_end)
        player.seek(2)
        self.assertFalse(player.at_start)
        self.assertTrue(player.at_end)


class TestSnapshot(unittest.TestCase):
    def test_snapshot_reflects_current_state(self):
        player = Player(4)
        player.seek(2)
        player.play()
        snapshot = player.snapshot()
        self.assertEqual(snapshot, PlayerState(index=2, playing=True))

    def test_snapshot_is_independent_of_later_mutation(self):
        player = Player(4)
        snapshot = player.snapshot()
        player.seek(3)
        self.assertEqual(snapshot.index, 0)
        self.assertEqual(player.index, 3)


if __name__ == "__main__":
    unittest.main()
