#!/usr/bin/env python
# coding: utf-8

# In[16]:


#!/usr/bin/env python
# coding: utf-8
"""
This script aims to work for creation of a lowdefy yaml from excel sheet
"""


# import json
import os
import sys
from datetime import datetime
from pprint import pprint

from pytz import timezone
from jinja2 import Environment, FileSystemLoader

import pandas as pd
import gdown


# script defaults
EXCEL_LOCAL_NAME = "websheets.xlsx"

# default WebSheet to get values from, if GOOGLE_SHEETS_URL env is not set
DEFAULT_EXCEL_URL = "https://drive.google.com/file/d/17YiHNPSh8STfk1d6ZBjkvstJ_ZHLrrSd/view?usp=sharing"

# gets GOOGLE_SHEETS_URL env variable or defaults to the above LINK
URL_TO_DOWNLOAD = os.getenv("GOOGLE_SHEETS_URL", DEFAULT_EXCEL_URL)

# root folder for all templates
TEMPLATES_DIR = "templates/"

# DEFAULT VAR for title based icon
ICON_TITLE = "yes"

# root folder for all Lowdefy YAML's
# or
# dir for all YAML's generated from this script
OUTPUT_DIR = "output/"

# change
LOWDEFY_VERSION = "3.18.0"

# all items in "lower" case
VERTICAL_MENUS = ["layout", "menuitems", "social"]

DEFAULT_IMG = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/meteor.svg'

IMAGES_DICT = {
    "fontawesome": 
        [ {"source": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/",
          "current_list": ['ad.svg', 'address-book.svg', 'address-card.svg', 'adjust.svg', 'air-freshener.svg', 'align-center.svg', 'align-justify.svg', 'align-left.svg', 'align-right.svg', 'allergies.svg', 'ambulance.svg', 'american-sign-language-interpreting.svg', 'anchor.svg', 'angle-double-down.svg', 'angle-double-left.svg', 'angle-double-right.svg', 'angle-double-up.svg', 'angle-down.svg', 'angle-left.svg', 'angle-right.svg', 'angle-up.svg', 'angry.svg', 'ankh.svg', 'apple-alt.svg', 'archive.svg', 'archway.svg', 'arrow-alt-circle-down.svg', 'arrow-alt-circle-left.svg', 'arrow-alt-circle-right.svg', 'arrow-alt-circle-up.svg', 'arrow-circle-down.svg', 'arrow-circle-left.svg', 'arrow-circle-right.svg', 'arrow-circle-up.svg', 'arrow-down.svg', 'arrow-left.svg', 'arrow-right.svg', 'arrow-up.svg', 'arrows-alt-h.svg', 'arrows-alt-v.svg', 'arrows-alt.svg', 'assistive-listening-systems.svg', 'asterisk.svg', 'at.svg', 'atlas.svg', 'atom.svg', 'audio-description.svg', 'award.svg', 'baby-carriage.svg', 'baby.svg', 'backspace.svg', 'backward.svg', 'bacon.svg', 'bacteria.svg', 'bacterium.svg', 'bahai.svg', 'balance-scale-left.svg', 'balance-scale-right.svg', 'balance-scale.svg', 'ban.svg', 'band-aid.svg', 'barcode.svg', 'bars.svg', 'baseball-ball.svg', 'basketball-ball.svg', 'bath.svg', 'battery-empty.svg', 'battery-full.svg', 'battery-half.svg', 'battery-quarter.svg', 'battery-three-quarters.svg', 'bed.svg', 'beer.svg', 'bell-slash.svg', 'bell.svg', 'bezier-curve.svg', 'bible.svg', 'bicycle.svg', 'biking.svg', 'binoculars.svg', 'biohazard.svg', 'birthday-cake.svg', 'blender-phone.svg', 'blender.svg', 'blind.svg', 'blog.svg', 'bold.svg', 'bolt.svg', 'bomb.svg', 'bone.svg', 'bong.svg', 'book-dead.svg', 'book-medical.svg', 'book-open.svg', 'book-reader.svg', 'book.svg', 'bookmark.svg', 'border-all.svg', 'border-none.svg', 'border-style.svg', 'bowling-ball.svg', 'box-open.svg', 'box-tissue.svg', 'box.svg', 'boxes.svg', 'braille.svg', 'brain.svg', 'bread-slice.svg', 'briefcase-medical.svg', 'briefcase.svg', 'broadcast-tower.svg', 'broom.svg', 'brush.svg', 'bug.svg', 'building.svg', 'bullhorn.svg', 'bullseye.svg', 'burn.svg', 'bus-alt.svg', 'bus.svg', 'business-time.svg', 'calculator.svg', 'calendar-alt.svg', 'calendar-check.svg', 'calendar-day.svg', 'calendar-minus.svg', 'calendar-plus.svg', 'calendar-times.svg', 'calendar-week.svg', 'calendar.svg', 'camera-retro.svg', 'camera.svg', 'campground.svg', 'candy-cane.svg', 'cannabis.svg', 'capsules.svg', 'car-alt.svg', 'car-battery.svg', 'car-crash.svg', 'car-side.svg', 'car.svg', 'caravan.svg', 
'caret-down.svg', 'caret-left.svg', 'caret-right.svg', 'caret-square-down.svg', 'caret-square-left.svg', 'caret-square-right.svg', 'caret-square-up.svg', 'caret-up.svg', 'carrot.svg', 'cart-arrow-down.svg', 'cart-plus.svg', 'cash-register.svg', 'cat.svg', 'certificate.svg', 'chair.svg', 'chalkboard-teacher.svg', 'chalkboard.svg', 'charging-station.svg', 'chart-area.svg', 'chart-bar.svg', 'chart-line.svg', 'chart-pie.svg', 'check-circle.svg', 'check-double.svg', 'check-square.svg', 'check.svg', 'cheese.svg', 'chess-bishop.svg', 'chess-board.svg', 'chess-king.svg', 'chess-knight.svg', 'chess-pawn.svg', 'chess-queen.svg', 'chess-rook.svg', 'chess.svg', 'chevron-circle-down.svg', 'chevron-circle-left.svg', 'chevron-circle-right.svg', 'chevron-circle-up.svg', 'chevron-down.svg', 'chevron-left.svg', 'chevron-right.svg', 'chevron-up.svg', 'child.svg', 'church.svg', 'circle-notch.svg', 'circle.svg', 'city.svg', 'clinic-medical.svg', 'clipboard-check.svg', 'clipboard-list.svg', 'clipboard.svg', 'clock.svg', 'clone.svg', 'closed-captioning.svg', 'cloud-download-alt.svg', 'cloud-meatball.svg', 'cloud-moon-rain.svg', 'cloud-moon.svg', 'cloud-rain.svg', 'cloud-showers-heavy.svg', 'cloud-sun-rain.svg', 'cloud-sun.svg', 'cloud-upload-alt.svg', 'cloud.svg', 'cocktail.svg', 'code-branch.svg', 'code.svg', 'coffee.svg', 'cog.svg', 'cogs.svg', 'coins.svg', 'columns.svg', 'comment-alt.svg', 'comment-dollar.svg', 'comment-dots.svg', 'comment-medical.svg', 'comment-slash.svg', 'comment.svg', 'comments-dollar.svg', 'comments.svg', 'compact-disc.svg', 'compass.svg', 'compress-alt.svg', 'compress-arrows-alt.svg', 'compress.svg', 'concierge-bell.svg', 'cookie-bite.svg', 'cookie.svg', 'copy.svg', 'copyright.svg', 'couch.svg', 'credit-card.svg', 'crop-alt.svg', 'crop.svg', 'cross.svg', 'crosshairs.svg', 'crow.svg', 'crown.svg', 'crutch.svg', 'cube.svg', 'cubes.svg', 'cut.svg', 'database.svg', 'deaf.svg', 'democrat.svg', 'desktop.svg', 'dharmachakra.svg', 'diagnoses.svg', 'dice-d20.svg', 'dice-d6.svg', 'dice-five.svg', 'dice-four.svg', 'dice-one.svg', 'dice-six.svg', 'dice-three.svg', 'dice-two.svg', 'dice.svg', 'digital-tachograph.svg', 'directions.svg', 'disease.svg', 'divide.svg', 'dizzy.svg', 'dna.svg', 'dog.svg', 'dollar-sign.svg', 'dolly-flatbed.svg', 'dolly.svg', 'donate.svg', 'door-closed.svg', 'door-open.svg', 'dot-circle.svg', 'dove.svg', 'download.svg', 'drafting-compass.svg', 'dragon.svg', 'draw-polygon.svg', 'drum-steelpan.svg', 'drum.svg', 'drumstick-bite.svg', 'dumbbell.svg', 'dumpster-fire.svg', 'dumpster.svg', 'dungeon.svg', 'edit.svg', 'egg.svg', 'eject.svg', 'ellipsis-h.svg', 'ellipsis-v.svg', 'envelope-open-text.svg', 'envelope-open.svg', 'envelope-square.svg', 'envelope.svg', 'equals.svg', 
'eraser.svg', 'ethernet.svg', 'euro-sign.svg', 'exchange-alt.svg', 'exclamation-circle.svg', 'exclamation-triangle.svg', 'exclamation.svg', 'expand-alt.svg', 'expand-arrows-alt.svg', 'expand.svg', 'external-link-alt.svg', 'external-link-square-alt.svg', 'eye-dropper.svg', 'eye-slash.svg', 'eye.svg', 'fan.svg', 'fast-backward.svg', 'fast-forward.svg', 'faucet.svg', 'fax.svg', 'feather-alt.svg', 'feather.svg', 'female.svg', 'fighter-jet.svg', 'file-alt.svg', 'file-archive.svg', 'file-audio.svg', 'file-code.svg', 'file-contract.svg', 'file-csv.svg', 'file-download.svg', 'file-excel.svg', 'file-export.svg', 'file-image.svg', 'file-import.svg', 'file-invoice-dollar.svg', 'file-invoice.svg', 'file-medical-alt.svg', 'file-medical.svg', 'file-pdf.svg', 'file-powerpoint.svg', 'file-prescription.svg', 'file-signature.svg', 'file-upload.svg', 'file-video.svg', 'file-word.svg', 'file.svg', 'fill-drip.svg', 'fill.svg', 'film.svg', 'filter.svg', 'fingerprint.svg', 'fire-alt.svg', 'fire-extinguisher.svg', 'fire.svg', 'first-aid.svg', 'fish.svg', 'fist-raised.svg', 'flag-checkered.svg', 'flag-usa.svg', 'flag.svg', 'flask.svg', 'flushed.svg', 'folder-minus.svg', 'folder-open.svg', 'folder-plus.svg', 'folder.svg', 'font-awesome-logo-full.svg', 'font.svg', 'football-ball.svg', 'forward.svg', 'frog.svg', 'frown-open.svg', 'frown.svg', 'funnel-dollar.svg', 'futbol.svg', 'gamepad.svg', 'gas-pump.svg', 'gavel.svg', 'gem.svg', 'genderless.svg', 'ghost.svg', 'gift.svg', 'gifts.svg', 'glass-cheers.svg', 'glass-martini-alt.svg', 'glass-martini.svg', 'glass-whiskey.svg', 'glasses.svg', 'globe-africa.svg', 'globe-americas.svg', 'globe-asia.svg', 'globe-europe.svg', 'globe.svg', 'golf-ball.svg', 'gopuram.svg', 'graduation-cap.svg', 'greater-than-equal.svg', 'greater-than.svg', 'grimace.svg', 'grin-alt.svg', 'grin-beam-sweat.svg', 'grin-beam.svg', 'grin-hearts.svg', 'grin-squint-tears.svg', 'grin-squint.svg', 'grin-stars.svg', 'grin-tears.svg', 'grin-tongue-squint.svg', 'grin-tongue-wink.svg', 'grin-tongue.svg', 'grin-wink.svg', 'grin.svg', 'grip-horizontal.svg', 'grip-lines-vertical.svg', 'grip-lines.svg', 'grip-vertical.svg', 'guitar.svg', 'h-square.svg', 'hamburger.svg', 'hammer.svg', 'hamsa.svg', 'hand-holding-heart.svg', 'hand-holding-medical.svg', 'hand-holding-usd.svg', 'hand-holding-water.svg', 'hand-holding.svg', 'hand-lizard.svg', 'hand-middle-finger.svg', 'hand-paper.svg', 'hand-peace.svg', 'hand-point-down.svg', 'hand-point-left.svg', 'hand-point-right.svg', 'hand-point-up.svg', 'hand-pointer.svg', 'hand-rock.svg', 'hand-scissors.svg', 'hand-sparkles.svg', 'hand-spock.svg', 'hands-helping.svg', 'hands-wash.svg', 'hands.svg', 'handshake-alt-slash.svg', 'handshake-slash.svg', 'handshake.svg', 'hanukiah.svg', 'hard-hat.svg', 'hashtag.svg', 'hat-cowboy-side.svg', 'hat-cowboy.svg', 'hat-wizard.svg', 'hdd.svg', 'head-side-cough-slash.svg', 'head-side-cough.svg', 'head-side-mask.svg', 
'head-side-virus.svg', 'heading.svg', 'headphones-alt.svg', 'headphones.svg', 'headset.svg', 'heart-broken.svg', 'heart.svg', 'heartbeat.svg', 'helicopter.svg', 'highlighter.svg', 'hiking.svg', 'hippo.svg', 'history.svg', 'hockey-puck.svg', 'holly-berry.svg', 'home.svg', 'horse-head.svg', 'horse.svg', 'hospital-alt.svg', 'hospital-symbol.svg', 'hospital-user.svg', 'hospital.svg', 'hot-tub.svg', 'hotdog.svg', 'hotel.svg', 'hourglass-end.svg', 'hourglass-half.svg', 'hourglass-start.svg', 'hourglass.svg', 'house-damage.svg', 'house-user.svg', 
'hryvnia.svg', 'i-cursor.svg', 'ice-cream.svg', 'icicles.svg', 'icons.svg', 'id-badge.svg', 'id-card-alt.svg', 'id-card.svg', 'igloo.svg', 'image.svg', 'images.svg', 'inbox.svg', 'indent.svg', 'industry.svg', 'infinity.svg', 'info-circle.svg', 'info.svg', 'italic.svg', 'jedi.svg', 'joint.svg', 'journal-whills.svg', 'kaaba.svg', 'key.svg', 'keyboard.svg', 'khanda.svg', 'kiss-beam.svg', 'kiss-wink-heart.svg', 'kiss.svg', 'kiwi-bird.svg', 'landmark.svg', 'language.svg', 'laptop-code.svg', 'laptop-house.svg', 'laptop-medical.svg', 'laptop.svg', 'laugh-beam.svg', 'laugh-squint.svg', 'laugh-wink.svg', 'laugh.svg', 'layer-group.svg', 'leaf.svg', 'lemon.svg', 'less-than-equal.svg', 'less-than.svg', 'level-down-alt.svg', 'level-up-alt.svg', 'life-ring.svg', 'lightbulb.svg', 'link.svg', 'lira-sign.svg', 'list-alt.svg', 'list-ol.svg', 'list-ul.svg', 'list.svg', 'location-arrow.svg', 'lock-open.svg', 'lock.svg', 'long-arrow-alt-down.svg', 'long-arrow-alt-left.svg', 'long-arrow-alt-right.svg', 'long-arrow-alt-up.svg', 'low-vision.svg', 'luggage-cart.svg', 'lungs-virus.svg', 'lungs.svg', 'magic.svg', 'magnet.svg', 'mail-bulk.svg', 'male.svg', 'map-marked-alt.svg', 'map-marked.svg', 'map-marker-alt.svg', 'map-marker.svg', 'map-pin.svg', 'map-signs.svg', 'map.svg', 'marker.svg', 'mars-double.svg', 'mars-stroke-h.svg', 'mars-stroke-v.svg', 'mars-stroke.svg', 'mars.svg', 'mask.svg', 'medal.svg', 'medkit.svg', 'meh-blank.svg', 'meh-rolling-eyes.svg', 
'meh.svg', 'memory.svg', 'menorah.svg', 'mercury.svg', 'meteor.svg', 'microchip.svg', 'microphone-alt-slash.svg', 'microphone-alt.svg', 'microphone-slash.svg', 'microphone.svg', 'microscope.svg', 'minus-circle.svg', 'minus-square.svg', 'minus.svg', 'mitten.svg', 'mobile-alt.svg', 'mobile.svg', 'money-bill-alt.svg', 'money-bill-wave-alt.svg', 'money-bill-wave.svg', 'money-bill.svg', 'money-check-alt.svg', 'money-check.svg', 'monument.svg', 'moon.svg', 'mortar-pestle.svg', 'mosque.svg', 'motorcycle.svg', 'mountain.svg', 'mouse-pointer.svg', 'mouse.svg', 'mug-hot.svg', 'music.svg', 'network-wired.svg', 'neuter.svg', 'newspaper.svg', 'not-equal.svg', 'notes-medical.svg', 'object-group.svg', 'object-ungroup.svg', 'oil-can.svg', 'om.svg', 'otter.svg', 'outdent.svg', 'pager.svg', 'paint-brush.svg', 'paint-roller.svg', 'palette.svg', 'pallet.svg', 'paper-plane.svg', 'paperclip.svg', 'parachute-box.svg', 'paragraph.svg', 'parking.svg', 'passport.svg', 'pastafarianism.svg', 'paste.svg', 'pause-circle.svg', 'pause.svg', 'paw.svg', 'peace.svg', 'pen-alt.svg', 'pen-fancy.svg', 'pen-nib.svg', 'pen-square.svg', 'pen.svg', 'pencil-alt.svg', 'pencil-ruler.svg', 'people-arrows.svg', 'people-carry.svg', 'pepper-hot.svg', 'percent.svg', 'percentage.svg', 'person-booth.svg', 'phone-alt.svg', 'phone-slash.svg', 'phone-square-alt.svg', 'phone-square.svg', 'phone-volume.svg', 'phone.svg', 'photo-video.svg', 'piggy-bank.svg', 'pills.svg', 'pizza-slice.svg', 'place-of-worship.svg', 'plane-arrival.svg', 'plane-departure.svg', 'plane-slash.svg', 'plane.svg', 'play-circle.svg', 'play.svg', 'plug.svg', 'plus-circle.svg', 'plus-square.svg', 
'plus.svg', 'podcast.svg', 'poll-h.svg', 'poll.svg', 'poo-storm.svg', 'poo.svg', 'poop.svg', 'portrait.svg', 'pound-sign.svg', 'power-off.svg', 'pray.svg', 'praying-hands.svg', 'prescription-bottle-alt.svg', 'prescription-bottle.svg', 'prescription.svg', 'print.svg', 'procedures.svg', 'project-diagram.svg', 'pump-medical.svg', 'pump-soap.svg', 'puzzle-piece.svg', 'qrcode.svg', 'question-circle.svg', 'question.svg', 'quidditch.svg', 'quote-left.svg', 'quote-right.svg', 'quran.svg', 'radiation-alt.svg', 'radiation.svg', 'rainbow.svg', 'random.svg', 'receipt.svg', 'record-vinyl.svg', 'recycle.svg', 'redo-alt.svg', 'redo.svg', 'registered.svg', 'remove-format.svg', 'reply-all.svg', 'reply.svg', 'republican.svg', 'restroom.svg', 'retweet.svg', 'ribbon.svg', 'ring.svg', 'road.svg', 'robot.svg', 'rocket.svg', 'route.svg', 'rss-square.svg', 'rss.svg', 'ruble-sign.svg', 'ruler-combined.svg', 'ruler-horizontal.svg', 'ruler-vertical.svg', 'ruler.svg', 'running.svg', 'rupee-sign.svg', 'sad-cry.svg', 'sad-tear.svg', 'satellite-dish.svg', 'satellite.svg', 'save.svg', 'school.svg', 'screwdriver.svg', 'scroll.svg', 'sd-card.svg', 'search-dollar.svg', 'search-location.svg', 'search-minus.svg', 'search-plus.svg', 'search.svg', 'seedling.svg', 'server.svg', 'shapes.svg', 'share-alt-square.svg', 'share-alt.svg', 'share-square.svg', 'share.svg', 'shekel-sign.svg', 'shield-alt.svg', 'shield-virus.svg', 'ship.svg', 'shipping-fast.svg', 'shoe-prints.svg', 
'shopping-bag.svg', 'shopping-basket.svg', 'shopping-cart.svg', 'shower.svg', 'shuttle-van.svg', 'sign-in-alt.svg', 'sign-language.svg', 'sign-out-alt.svg', 'sign.svg', 'signal.svg', 'signature.svg', 'sim-card.svg', 'sink.svg', 'sitemap.svg', 'skating.svg', 'skiing-nordic.svg', 'skiing.svg', 'skull-crossbones.svg', 'skull.svg', 'slash.svg', 'sleigh.svg', 'sliders-h.svg', 'smile-beam.svg', 'smile-wink.svg', 'smile.svg', 'smog.svg', 'smoking-ban.svg', 'smoking.svg', 'sms.svg', 'snowboarding.svg', 'snowflake.svg', 'snowman.svg', 'snowplow.svg', 'soap.svg', 'socks.svg', 'solar-panel.svg', 'sort-alpha-down-alt.svg', 'sort-alpha-down.svg', 'sort-alpha-up-alt.svg', 'sort-alpha-up.svg', 'sort-amount-down-alt.svg', 'sort-amount-down.svg', 'sort-amount-up-alt.svg', 'sort-amount-up.svg', 'sort-down.svg', 'sort-numeric-down-alt.svg', 'sort-numeric-down.svg', 'sort-numeric-up-alt.svg', 'sort-numeric-up.svg', 'sort-up.svg', 'sort.svg', 'spa.svg', 'space-shuttle.svg', 'spell-check.svg', 'spider.svg', 'spinner.svg', 'splotch.svg', 'spray-can.svg', 'square-full.svg', 'square-root-alt.svg', 'square.svg', 'stamp.svg', 'star-and-crescent.svg', 'star-half-alt.svg', 'star-half.svg', 'star-of-david.svg', 'star-of-life.svg', 'star.svg', 'step-backward.svg', 'step-forward.svg', 
'stethoscope.svg', 'sticky-note.svg', 'stop-circle.svg', 'stop.svg', 'stopwatch-20.svg', 'stopwatch.svg', 'store-alt-slash.svg', 'store-alt.svg', 'store-slash.svg', 'store.svg', 'stream.svg', 'street-view.svg', 'strikethrough.svg', 'stroopwafel.svg', 'subscript.svg', 'subway.svg', 'suitcase-rolling.svg', 'suitcase.svg', 'sun.svg', 'superscript.svg', 'surprise.svg', 'swatchbook.svg', 'swimmer.svg', 'swimming-pool.svg', 'synagogue.svg', 'sync-alt.svg', 'sync.svg', 'syringe.svg', 'table-tennis.svg', 'table.svg', 'tablet-alt.svg', 'tablet.svg', 'tablets.svg', 'tachometer-alt.svg', 'tag.svg', 'tags.svg', 'tape.svg', 'tasks.svg', 'taxi.svg', 'teeth-open.svg', 'teeth.svg', 'temperature-high.svg', 'temperature-low.svg', 'tenge.svg', 'terminal.svg', 'text-height.svg', 'text-width.svg', 'th-large.svg', 'th-list.svg', 'th.svg', 'theater-masks.svg', 'thermometer-empty.svg', 'thermometer-full.svg', 'thermometer-half.svg', 'thermometer-quarter.svg', 'thermometer-three-quarters.svg', 'thermometer.svg', 'thumbs-down.svg', 'thumbs-up.svg', 'thumbtack.svg', 'ticket-alt.svg', 'times-circle.svg', 'times.svg', 'tint-slash.svg', 'tint.svg', 'tired.svg', 'toggle-off.svg', 'toggle-on.svg', 'toilet-paper-slash.svg', 'toilet-paper.svg', 'toilet.svg', 'toolbox.svg', 'tools.svg', 'tooth.svg', 'torah.svg', 'torii-gate.svg', 'tractor.svg', 'trademark.svg', 'traffic-light.svg', 'trailer.svg', 'train.svg', 'tram.svg', 'transgender-alt.svg', 'transgender.svg', 'trash-alt.svg', 'trash-restore-alt.svg', 'trash-restore.svg', 'trash.svg', 'tree.svg', 'trophy.svg', 'truck-loading.svg', 'truck-monster.svg', 'truck-moving.svg', 'truck-pickup.svg', 'truck.svg', 'tshirt.svg', 'tty.svg', 'tv.svg', 'umbrella-beach.svg', 'umbrella.svg', 'underline.svg', 'undo-alt.svg', 'undo.svg', 'universal-access.svg', 'university.svg', 'unlink.svg', 'unlock-alt.svg', 'unlock.svg', 'upload.svg', 'user-alt-slash.svg', 'user-alt.svg', 'user-astronaut.svg', 'user-check.svg', 'user-circle.svg', 'user-clock.svg', 'user-cog.svg', 'user-edit.svg', 'user-friends.svg', 'user-graduate.svg', 'user-injured.svg', 'user-lock.svg', 'user-md.svg', 'user-minus.svg', 'user-ninja.svg', 'user-nurse.svg', 'user-plus.svg', 'user-secret.svg', 'user-shield.svg', 'user-slash.svg', 'user-tag.svg', 'user-tie.svg', 'user-times.svg', 'user.svg', 'users-cog.svg', 'users-slash.svg', 'users.svg', 'utensil-spoon.svg', 'utensils.svg', 'vector-square.svg', 'venus-double.svg', 'venus-mars.svg', 'venus.svg', 'vest-patches.svg', 'vest.svg', 'vial.svg', 'vials.svg', 'video-slash.svg', 'video.svg', 'vihara.svg', 'virus-slash.svg', 'virus.svg', 'viruses.svg', 'voicemail.svg', 'volleyball-ball.svg', 'volume-down.svg', 'volume-mute.svg', 'volume-off.svg', 'volume-up.svg', 'vote-yea.svg', 'vr-cardboard.svg', 'walking.svg', 'wallet.svg', 'warehouse.svg', 'water.svg', 'wave-square.svg', 'weight-hanging.svg', 'weight.svg', 'wheelchair.svg', 'wifi.svg', 'wind.svg', 
'window-close.svg', 'window-maximize.svg', 'window-minimize.svg', 'window-restore.svg', 'wine-bottle.svg', 'wine-glass-alt.svg', 'wine-glass.svg', 'won-sign.svg', 'wrench.svg', 'x-ray.svg', 'yen-sign.svg', 'yin-yang.svg']
        },
    {"source":"","current_list":[]}    
    ]
}

def icon_finder(search_item):
    """
    Define doc here
    """
    for groups in IMAGES_DICT:
        for  items in IMAGES_DICT[groups]:
            for available_icons in items["current_list"]:
                if (search_item.lower() in available_icons.lower()):
                    return items["source"]+available_icons
    return DEFAULT_IMG

def get_jinja_dict(
        excel_loc="",
        xl_engine="openpyxl",
        vertical_menus=False,
        sheet="Layout"):
    """
    converts given excel sheet into dict/json
    groups content for Layout
    """
    data_frame = pd.read_excel(
        excel_loc,
        engine=xl_engine,
        sheet_name=sheet)
    # if it is a layout file, return as it is
    # else, read the rows and map to them as a dictionary
    if vertical_menus:
        ret_obj = {}
        for index, row in data_frame.iterrows():
            #             print(row)
            try:
                ret_obj.update({str(row[0]).strip(): str(row[1]).strip()})
            except Exception as error:
                print("IDENTIFIER", error)
        return ret_obj
    else:
        # rename Pandas columns to lower case
        data_frame.columns = data_frame.columns.str.lower()
        return data_frame.to_dict(orient='records')


def make_lowdefy_pages(templates_dir, output_dir, excel_loc):
    """
    generates Lowdefy pages, all but the homepage.
    """
    #   get dict for making lowdefy layout
    all_layout_config = get_jinja_dict(
        excel_loc, sheet="Home", vertical_menus=True)

    #   placeholder for all featured posts
    all_featured = {}

    #   update footer with time
    all_layout_config["footer_note"] = "Updated at " + \
        str(datetime.now(timezone('UTC'))).split(".")[0] + "  UTC"

#     pprint(get_jinja_dict(
#         excel_loc, sheet="Menu", vertical_menus= True))
    # being read from a different sheet but put into old
    all_layout_config["menuitem"] = get_jinja_dict(
        excel_loc, sheet="Menu", vertical_menus=True)

    all_layout_config["social"] = get_jinja_dict(
        excel_loc, sheet="Social", vertical_menus=True)

    pprint(all_layout_config)

    for page in all_layout_config["menuitem"].keys():
        try:
            posts = get_jinja_dict(
                excel_loc, sheet=page.capitalize())
            featured = []
            pinned = []
            count = 0
            all_posts_without_pinned = []
            for post in posts:
                count += 1
                abouts = {}
                for keys_about in post.keys():
                    if "extra_" in keys_about:
                        abouts.update(
                            {keys_about.split("_")[1]: post[keys_about]})
                    else:
                        continue

                post.update({"abouts": abouts})
                pprint(post.keys())
                if str(post["icon"]) == "nan":
                    print("No image for post", post["title"], page)
                    post["icon"] = False
                elif str(post["icon"]) != "nan" and str(post["icon"]).strip() != "" and str(post["icon"]) == ICON_TITLE:
                    #                     call function
                    print("Default icon chosen")
                     post["icon_source"] = post["icon"]
                     post["icon"] = True
                elif str(post["icon"]) != "nan" and str(post["icon"]).strip():
                    print("Default icon chosen")
                    post["icon_source"] = icon_finder(post["title"])
                        
                    post["icon"] = True
                else:
                    post["icon"] = False

                if str(post["featured"]).strip().lower() == "yes":
                    featured.append(post)

                if str(post["pinned"]).strip().lower() == "yes":
                    pinned.append(post)

                else:
                    all_posts_without_pinned.append(post)
                pprint(post)
            all_featured.update({page.capitalize(): featured})

            with open(r'{}/post.yaml'.format(templates_dir)) as file:
                home_list = file.read()
                print("reading file")
                j2_template = Environment(
                    loader=FileSystemLoader("templates/")).from_string(home_list)
                open("{}/{}.yaml".format(output_dir,
                                         page),
                     "w+").write(j2_template.render(title=page,
                                                    all_layout_config=all_layout_config,
                                                    posts=all_posts_without_pinned,
                                                    pinned=pinned))

        except Exception as error_generic:
            print(
                "Error",
                error_generic,
                "\nDid you forget to include a page which is mentioned in the `menuitems` ?")
            open("{}/{}.yaml".format(OUTPUT_DIR, page), "w+")
#     pprint(all_featured)
    with open(r'templates/home.yaml') as file:
        home_list = file.read()
        j2_template = Environment(loader=FileSystemLoader(
            "templates/")).from_string(home_list)
        open("{}/lowdefy.yaml".format(output_dir),
             "w+").write(j2_template.render(all_layout_config=all_layout_config,
                                            all_featured=all_featured))


def download_excel(url_input, output):
    """
    Downloads excel from google
    """
    try:
        url = 'https://drive.google.com/uc?id={}'.format(
            url_input.split("/")[-2])
        gdown.download(url, output, quiet=False)

    except Exception as error_generic:
        print(
            "Could not download the file. Please recheck the file/connection/url\n",
            error_generic)


try:
    download_excel(URL_TO_DOWNLOAD, EXCEL_LOCAL_NAME)
    make_lowdefy_pages(TEMPLATES_DIR, OUTPUT_DIR, EXCEL_LOCAL_NAME)

except Exception as error_generic:
    print("Unexpected error occured", error_generic)
    sys.exit(0)


# In[ ]:


# In[ ]:


# In[ ]:
