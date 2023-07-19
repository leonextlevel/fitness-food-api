from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command


def test_extract_products_command():
    out = StringIO()
    with patch(
        'fitness_food.products.management.commands.extract_products.urlopen'
    ) as mock_urlopen:
        mock_urlopen.return_value = 'html'
        with patch(
            'fitness_food.products.management.commands.extract_products'
            '.BeautifulSoup'
        ) as mock_bs:
            mock_bs.return_value = MagicMock()
            mock_bs.return_value.find.return_value = MagicMock()
            mock_bs.return_value.find.return_value.find_all.return_value = []
            call_command('extract_products', stdout=out)
            assert 'done' in out.getvalue()
