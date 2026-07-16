import pytest
from unittest.mock import AsyncMock, patch
from backend.services.alert_service import alert_service
from backend.models.alert import Alert

@pytest.mark.asyncio
async def test_get_alerts_service():
    mock_session = AsyncMock()
    
    mock_alert = Alert(id=1, status="NEW")
    
    with patch("backend.services.alert_service.alert_repo") as mock_repo:
        mock_repo.get_multi = AsyncMock(return_value=([mock_alert], 1))
        
        alerts, total = await alert_service.get_alerts(mock_session, skip=0, limit=10)
        
        assert len(alerts) == 1
        assert total == 1
        assert alerts[0].id == 1
        mock_repo.get_multi.assert_called_once_with(mock_session, skip=0, limit=10)

@pytest.mark.asyncio
async def test_update_alert_status():
    mock_session = AsyncMock()
    mock_alert = Alert(id=1, status="NEW")
    updated_alert = Alert(id=1, status="RESOLVED")
    
    with patch("backend.services.alert_service.alert_repo") as mock_repo:
        mock_repo.get = AsyncMock(return_value=mock_alert)
        mock_repo.update = AsyncMock(return_value=updated_alert)
        
        result = await alert_service.update_status(mock_session, alert_id=1, status="RESOLVED")
        
        assert result.status == "RESOLVED"
        mock_repo.get.assert_called_once_with(mock_session, 1)
        mock_repo.update.assert_called_once()
