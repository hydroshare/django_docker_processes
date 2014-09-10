from django.core.signals import Signal

process_finished = Signal(providing_args=['result_text', 'result_data', 'files', 'profile','logs'])
process_aborted = Signal(providing_args=['error_text','result_data','profile','logs'])
