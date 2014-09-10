from django.core.signals import Signal

process_completed = Signal(providing_args=['result_text', ''])
process_aborted = Signal(providing_args=[])
