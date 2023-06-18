from model.FilterChain import FilterChain


class Controller:
    def __init__(self, cli_arguments, cli_options):
        self.cli_arguments = cli_arguments
        self.cli_options = cli_options

    def run_conversion(self) -> int:
        filter_chain = FilterChain(self.cli_arguments['gpkg'], self.cli_arguments['clipsrc'])
        filtered_dictionaries = filter_chain.execute_filters()
        print(filtered_dictionaries)
