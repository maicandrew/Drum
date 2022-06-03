from asyncio import create_subprocess_shell
from pygame import mixer

mixer.init()

hi_hat_sound = mixer.Sound('sounds/hi hat.wav')
snare_sound = mixer.Sound('sounds/snare.wav')
kick_sound = mixer.Sound('sounds/kick.wav')
crash_sound = mixer.Sound('sounds/crash.wav')
clap_sound = mixer.Sound('sounds/clap.wav')
tom_sound = mixer.Sound('sounds/tom.wav')

inst_sounds = {
    0: hi_hat_sound,
    1: snare_sound,
    2: kick_sound,
    3: crash_sound,
    4: clap_sound,
    5: tom_sound
}
