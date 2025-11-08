package main

import (
	"github.com/kralamoure/retroproto/msgcli"
	"github.com/kralamoure/retroproto/msgsvr"
)

// ParserFn is the signature for message parser functions
type ParserFn func(s string) (interface{}, error)

// Registry contains all message parsers
var Registry = map[string]ParserFn{
	// AccountAddCharacter - msgcli\accountaddcharacter.go
	"AccountAddCharacter": func(s string) (interface{}, error) {
		return msgcli.NewAccountAddCharacter(s)
	},

	// AccountAskCharacterMigration - msgcli\accountaskcharactermigration.go
	"AccountAskCharacterMigration": func(s string) (interface{}, error) {
		return msgcli.NewAccountAskCharacterMigration(s)
	},

	// AccountAttributeGiftToCharacter - msgcli\accountattributegifttocharacter.go
	"AccountAttributeGiftToCharacter": func(s string) (interface{}, error) {
		return msgcli.NewAccountAttributeGiftToCharacter(s)
	},

	// AccountBoost - msgcli\accountboost.go
	"AccountBoost": func(s string) (interface{}, error) {
		return msgcli.NewAccountBoost(s)
	},

	// AccountCharacterAddError - msgsvr\accountcharacteradderror.go
	"AccountCharacterAddError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterAddError(s)
	},

	// AccountCharacterAddSuccess - msgsvr\accountcharacteraddsuccess.go
	"AccountCharacterAddSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterAddSuccess(s)
	},

	// AccountCharacterDeleteError - msgsvr\accountcharacterdeleteerror.go
	"AccountCharacterDeleteError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterDeleteError(s)
	},

	// AccountCharacterDeleteSuccess - msgsvr\accountcharacterdeletesuccess.go
	"AccountCharacterDeleteSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterDeleteSuccess(s)
	},

	// AccountCharacterMigrationAskConfirm - msgsvr\accountcharactermigrationaskconfirm.go
	"AccountCharacterMigrationAskConfirm": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterMigrationAskConfirm(s)
	},

	// AccountCharacterMigrationError - msgsvr\accountcharactermigrationerror.go
	"AccountCharacterMigrationError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterMigrationError(s)
	},

	// AccountCharacterMigrationSuccess - msgsvr\accountcharactermigrationsuccess.go
	"AccountCharacterMigrationSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterMigrationSuccess(s)
	},

	// AccountCharacterNameGeneratedError - msgsvr\accountcharacternamegeneratederror.go
	"AccountCharacterNameGeneratedError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterNameGeneratedError(s)
	},

	// AccountCharacterNameGeneratedSuccess - msgsvr\accountcharacternamegeneratedsuccess.go
	"AccountCharacterNameGeneratedSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterNameGeneratedSuccess(s)
	},

	// AccountCharacterSelectedError - msgsvr\accountcharacterselectederror.go
	"AccountCharacterSelectedError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterSelectedError(s)
	},

	// AccountCharacterSelectedSuccess - msgsvr\accountcharacterselectedsuccess.go
	"AccountCharacterSelectedSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharacterSelectedSuccess(s)
	},

	// AccountCharactersListError - msgsvr\accountcharacterslisterror.go
	"AccountCharactersListError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharactersListError(s)
	},

	// AccountCharactersListSuccess - msgsvr\accountcharacterslistsuccess.go
	"AccountCharactersListSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCharactersListSuccess(s)
	},

	// AccountCommunity - msgsvr\accountcommunity.go
	"AccountCommunity": func(s string) (interface{}, error) {
		return msgsvr.NewAccountCommunity(s)
	},

	// AccountConfiguredPort - msgcli\accountconfiguredport.go
	"AccountConfiguredPort": func(s string) (interface{}, error) {
		return msgcli.NewAccountConfiguredPort(s)
	},

	// AccountCredential - msgcli\accountcredential.go
	"AccountCredential": func(s string) (interface{}, error) {
		return msgcli.NewAccountCredential(s)
	},

	// AccountDeleteCharacter - msgcli\accountdeletecharacter.go
	"AccountDeleteCharacter": func(s string) (interface{}, error) {
		return msgcli.NewAccountDeleteCharacter(s)
	},

	// AccountDeleteCharacterMigration - msgcli\accountdeletecharactermigration.go
	"AccountDeleteCharacterMigration": func(s string) (interface{}, error) {
		return msgcli.NewAccountDeleteCharacterMigration(s)
	},

	// AccountFriendServerList - msgsvr\accountfriendserverlist.go
	"AccountFriendServerList": func(s string) (interface{}, error) {
		return msgsvr.NewAccountFriendServerList(s)
	},

	// AccountGetCharacters - msgcli\accountgetcharacters.go
	"AccountGetCharacters": func(s string) (interface{}, error) {
		return msgcli.NewAccountGetCharacters(s)
	},

	// AccountGetCharactersForced - msgcli\accountgetcharactersforced.go
	"AccountGetCharactersForced": func(s string) (interface{}, error) {
		return msgcli.NewAccountGetCharactersForced(s)
	},

	// AccountGetGifts - msgcli\accountgetgifts.go
	"AccountGetGifts": func(s string) (interface{}, error) {
		return msgcli.NewAccountGetGifts(s)
	},

	// AccountGetRandomCharacterName - msgcli\accountgetrandomcharactername.go
	"AccountGetRandomCharacterName": func(s string) (interface{}, error) {
		return msgcli.NewAccountGetRandomCharacterName(s)
	},

	// AccountGetServersList - msgcli\accountgetserverslist.go
	"AccountGetServersList": func(s string) (interface{}, error) {
		return msgcli.NewAccountGetServersList(s)
	},

	// AccountGiftStoredError - msgsvr\accountgiftstorederror.go
	"AccountGiftStoredError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountGiftStoredError(s)
	},

	// AccountGiftStoredSuccess - msgsvr\accountgiftstoredsuccess.go
	"AccountGiftStoredSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountGiftStoredSuccess(s)
	},

	// AccountGiftsList - msgsvr\accountgiftslist.go
	"AccountGiftsList": func(s string) (interface{}, error) {
		return msgsvr.NewAccountGiftsList(s)
	},

	// AccountHosts - msgsvr\accounthosts.go
	"AccountHosts": func(s string) (interface{}, error) {
		return msgsvr.NewAccountHosts(s)
	},

	// AccountKey - msgsvr\accountkey.go
	"AccountKey": func(s string) (interface{}, error) {
		return msgsvr.NewAccountKey(s)
	},

	// AccountLoginError - msgsvr\accountloginerror.go
	"AccountLoginError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountLoginError(s)
	},

	// AccountLoginSuccess - msgsvr\accountloginsuccess.go
	"AccountLoginSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountLoginSuccess(s)
	},

	// AccountMiniClipInfo - msgsvr\accountminiclipinfo.go
	"AccountMiniClipInfo": func(s string) (interface{}, error) {
		return msgsvr.NewAccountMiniClipInfo(s)
	},

	// AccountNewLevel - msgsvr\accountnewlevel.go
	"AccountNewLevel": func(s string) (interface{}, error) {
		return msgsvr.NewAccountNewLevel(s)
	},

	// AccountNewQueue - msgsvr\accountnewqueue.go
	"AccountNewQueue": func(s string) (interface{}, error) {
		return msgsvr.NewAccountNewQueue(s)
	},

	// AccountPseudo - msgsvr\accountpseudo.go
	"AccountPseudo": func(s string) (interface{}, error) {
		return msgsvr.NewAccountPseudo(s)
	},

	// AccountQueue - msgsvr\accountqueue.go
	"AccountQueue": func(s string) (interface{}, error) {
		return msgsvr.NewAccountQueue(s)
	},

	// AccountQueuePosition - msgcli\accountqueueposition.go
	"AccountQueuePosition": func(s string) (interface{}, error) {
		return msgcli.NewAccountQueuePosition(s)
	},

	// AccountRegionalVersion - msgsvr\accountregionalversion.go
	"AccountRegionalVersion": func(s string) (interface{}, error) {
		return msgsvr.NewAccountRegionalVersion(s)
	},

	// AccountRequestRegionalVersion - msgcli\accountrequestregionalversion.go
	"AccountRequestRegionalVersion": func(s string) (interface{}, error) {
		return msgcli.NewAccountRequestRegionalVersion(s)
	},

	// AccountRequestRescue - msgcli\accountrequestrescue.go
	"AccountRequestRescue": func(s string) (interface{}, error) {
		return msgcli.NewAccountRequestRescue(s)
	},

	// AccountRescue - msgsvr\accountrescue.go
	"AccountRescue": func(s string) (interface{}, error) {
		return msgsvr.NewAccountRescue(s)
	},

	// AccountResetCharacter - msgcli\accountresetcharacter.go
	"AccountResetCharacter": func(s string) (interface{}, error) {
		return msgcli.NewAccountResetCharacter(s)
	},

	// AccountRestrictions - msgsvr\accountrestrictions.go
	"AccountRestrictions": func(s string) (interface{}, error) {
		return msgsvr.NewAccountRestrictions(s)
	},

	// AccountSearchForFriend - msgcli\accountsearchforfriend.go
	"AccountSearchForFriend": func(s string) (interface{}, error) {
		return msgcli.NewAccountSearchForFriend(s)
	},

	// AccountSecretQuestion - msgsvr\accountsecretquestion.go
	"AccountSecretQuestion": func(s string) (interface{}, error) {
		return msgsvr.NewAccountSecretQuestion(s)
	},

	// AccountSelectServerError - msgsvr\accountselectservererror.go
	"AccountSelectServerError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountSelectServerError(s)
	},

	// AccountSelectServerPlainSuccess - msgsvr\accountselectserverplainsuccess.go
	"AccountSelectServerPlainSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountSelectServerPlainSuccess(s)
	},

	// AccountSelectServerSuccess - msgsvr\accountselectserversuccess.go
	"AccountSelectServerSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountSelectServerSuccess(s)
	},

	// AccountSendIdentity - msgcli\accountsendidentity.go
	"AccountSendIdentity": func(s string) (interface{}, error) {
		return msgcli.NewAccountSendIdentity(s)
	},

	// AccountSendTicket - msgcli\accountsendticket.go
	"AccountSendTicket": func(s string) (interface{}, error) {
		return msgcli.NewAccountSendTicket(s)
	},

	// AccountServersListError - msgsvr\accountserverslisterror.go
	"AccountServersListError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountServersListError(s)
	},

	// AccountServersListSuccess - msgsvr\accountserverslistsuccess.go
	"AccountServersListSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountServersListSuccess(s)
	},

	// AccountSetCharacter - msgcli\accountsetcharacter.go
	"AccountSetCharacter": func(s string) (interface{}, error) {
		return msgcli.NewAccountSetCharacter(s)
	},

	// AccountSetNickname - msgcli\accountsetnickname.go
	"AccountSetNickname": func(s string) (interface{}, error) {
		return msgcli.NewAccountSetNickname(s)
	},

	// AccountSetServer - msgcli\accountsetserver.go
	"AccountSetServer": func(s string) (interface{}, error) {
		return msgcli.NewAccountSetServer(s)
	},

	// AccountStats - msgsvr\accountstats.go
	"AccountStats": func(s string) (interface{}, error) {
		return msgsvr.NewAccountStats(s)
	},

	// AccountTicketResponseError - msgsvr\accountticketresponseerror.go
	"AccountTicketResponseError": func(s string) (interface{}, error) {
		return msgsvr.NewAccountTicketResponseError(s)
	},

	// AccountTicketResponseSuccess - msgsvr\accountticketresponsesuccess.go
	"AccountTicketResponseSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewAccountTicketResponseSuccess(s)
	},

	// AccountUseKey - msgcli\accountusekey.go
	"AccountUseKey": func(s string) (interface{}, error) {
		return msgcli.NewAccountUseKey(s)
	},

	// AccountValidCharacterMigration - msgcli\accountvalidcharactermigration.go
	"AccountValidCharacterMigration": func(s string) (interface{}, error) {
		return msgcli.NewAccountValidCharacterMigration(s)
	},

	// AccountVersion - msgcli\accountversion.go
	"AccountVersion": func(s string) (interface{}, error) {
		return msgcli.NewAccountVersion(s)
	},

	// AksHelloConnect - msgsvr\akshelloconnect.go
	"AksHelloConnect": func(s string) (interface{}, error) {
		return msgsvr.NewAksHelloConnect(s)
	},

	// AksHelloGame - msgsvr\akshellogame.go
	"AksHelloGame": func(s string) (interface{}, error) {
		return msgsvr.NewAksHelloGame(s)
	},

	// AksPing - msgcli\aksping.go
	"AksPing": func(s string) (interface{}, error) {
		return msgcli.NewAksPing(s)
	},

	// AksPong - msgsvr\akspong.go
	"AksPong": func(s string) (interface{}, error) {
		return msgsvr.NewAksPong(s)
	},

	// AksQuickPing - msgcli\aksquickping.go
	"AksQuickPing": func(s string) (interface{}, error) {
		return msgcli.NewAksQuickPing(s)
	},

	// AksQuickPong - msgsvr\aksquickpong.go
	"AksQuickPong": func(s string) (interface{}, error) {
		return msgsvr.NewAksQuickPong(s)
	},

	// AksRPing - msgsvr\aksrping.go
	"AksRPing": func(s string) (interface{}, error) {
		return msgsvr.NewAksRPing(s)
	},

	// AksRPong - msgcli\aksrpong.go
	"AksRPong": func(s string) (interface{}, error) {
		return msgcli.NewAksRPong(s)
	},

	// AksServerMessage - msgsvr\aksservermessage.go
	"AksServerMessage": func(s string) (interface{}, error) {
		return msgsvr.NewAksServerMessage(s)
	},

	// AksServerWillDisconnect - msgsvr\aksserverwilldisconnect.go
	"AksServerWillDisconnect": func(s string) (interface{}, error) {
		return msgsvr.NewAksServerWillDisconnect(s)
	},

	// BasicsAuthorizedCommand - msgcli\basicsauthorizedcommand.go
	"BasicsAuthorizedCommand": func(s string) (interface{}, error) {
		return msgcli.NewBasicsAuthorizedCommand(s)
	},

	// BasicsAuthorizedCommandClear - msgsvr\basicsauthorizedcommandclear.go
	"BasicsAuthorizedCommandClear": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAuthorizedCommandClear(s)
	},

	// BasicsAuthorizedCommandError - msgsvr\basicsauthorizedcommanderror.go
	"BasicsAuthorizedCommandError": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAuthorizedCommandError(s)
	},

	// BasicsAuthorizedCommandPrompt - msgsvr\basicsauthorizedcommandprompt.go
	"BasicsAuthorizedCommandPrompt": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAuthorizedCommandPrompt(s)
	},

	// BasicsAuthorizedCommandSuccess - msgsvr\basicsauthorizedcommandsuccess.go
	"BasicsAuthorizedCommandSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAuthorizedCommandSuccess(s)
	},

	// BasicsAuthorizedInterfaceClose - msgsvr\basicsauthorizedinterfaceclose.go
	"BasicsAuthorizedInterfaceClose": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAuthorizedInterfaceClose(s)
	},

	// BasicsAuthorizedInterfaceOpen - msgsvr\basicsauthorizedinterfaceopen.go
	"BasicsAuthorizedInterfaceOpen": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAuthorizedInterfaceOpen(s)
	},

	// BasicsAuthorizedKickCommand - msgcli\basicsauthorizedkickcommand.go
	"BasicsAuthorizedKickCommand": func(s string) (interface{}, error) {
		return msgcli.NewBasicsAuthorizedKickCommand(s)
	},

	// BasicsAuthorizedLine - msgsvr\basicsauthorizedline.go
	"BasicsAuthorizedLine": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAuthorizedLine(s)
	},

	// BasicsAuthorizedMoveCommand - msgcli\basicsauthorizedmovecommand.go
	"BasicsAuthorizedMoveCommand": func(s string) (interface{}, error) {
		return msgcli.NewBasicsAuthorizedMoveCommand(s)
	},

	// BasicsAveragePing - msgsvr\basicsaverageping.go
	"BasicsAveragePing": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsAveragePing(s)
	},

	// BasicsAway - msgcli\basicsaway.go
	"BasicsAway": func(s string) (interface{}, error) {
		return msgcli.NewBasicsAway(s)
	},

	// BasicsDate - msgsvr\basicsdate.go
	"BasicsDate": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsDate(s)
	},

	// BasicsFileCheck - msgsvr\basicsfilecheck.go
	"BasicsFileCheck": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsFileCheck(s)
	},

	// BasicsFileCheckAnswer - msgcli\basicsfilecheckanswer.go
	"BasicsFileCheckAnswer": func(s string) (interface{}, error) {
		return msgcli.NewBasicsFileCheckAnswer(s)
	},

	// BasicsGetDate - msgcli\basicsgetdate.go
	"BasicsGetDate": func(s string) (interface{}, error) {
		return msgcli.NewBasicsGetDate(s)
	},

	// BasicsInvisible - msgcli\basicsinvisible.go
	"BasicsInvisible": func(s string) (interface{}, error) {
		return msgcli.NewBasicsInvisible(s)
	},

	// BasicsKick - msgcli\basicskick.go
	"BasicsKick": func(s string) (interface{}, error) {
		return msgcli.NewBasicsKick(s)
	},

	// BasicsNothing - msgsvr\basicsnothing.go
	"BasicsNothing": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsNothing(s)
	},

	// BasicsRequestAveragePing - msgcli\basicsrequestaverageping.go
	"BasicsRequestAveragePing": func(s string) (interface{}, error) {
		return msgcli.NewBasicsRequestAveragePing(s)
	},

	// BasicsSanctionMe - msgcli\basicssanctionme.go
	"BasicsSanctionMe": func(s string) (interface{}, error) {
		return msgcli.NewBasicsSanctionMe(s)
	},

	// BasicsSubscriberRestrictionAdd - msgsvr\basicssubscriberrestrictionadd.go
	"BasicsSubscriberRestrictionAdd": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsSubscriberRestrictionAdd(s)
	},

	// BasicsSubscriberRestrictionRemove - msgsvr\basicssubscriberrestrictionremove.go
	"BasicsSubscriberRestrictionRemove": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsSubscriberRestrictionRemove(s)
	},

	// BasicsTime - msgsvr\basicstime.go
	"BasicsTime": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsTime(s)
	},

	// BasicsWhoIs - msgcli\basicswhois.go
	"BasicsWhoIs": func(s string) (interface{}, error) {
		return msgcli.NewBasicsWhoIs(s)
	},

	// BasicsWhoIsError - msgsvr\basicswhoiserror.go
	"BasicsWhoIsError": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsWhoIsError(s)
	},

	// BasicsWhoIsSuccess - msgsvr\basicswhoissuccess.go
	"BasicsWhoIsSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewBasicsWhoIsSuccess(s)
	},

	// ChatMessageError - msgsvr\chatmessageerror.go
	"ChatMessageError": func(s string) (interface{}, error) {
		return msgsvr.NewChatMessageError(s)
	},

	// ChatMessageSuccess - msgsvr\chatmessagesuccess.go
	"ChatMessageSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewChatMessageSuccess(s)
	},

	// ChatReportMessage - msgcli\chatreportmessage.go
	"ChatReportMessage": func(s string) (interface{}, error) {
		return msgcli.NewChatReportMessage(s)
	},

	// ChatRequestSubscribeChannelAdd - msgcli\chatrequestsubscribechanneladd.go
	"ChatRequestSubscribeChannelAdd": func(s string) (interface{}, error) {
		return msgcli.NewChatRequestSubscribeChannelAdd(s)
	},

	// ChatRequestSubscribeChannelRemove - msgcli\chatrequestsubscribechannelremove.go
	"ChatRequestSubscribeChannelRemove": func(s string) (interface{}, error) {
		return msgcli.NewChatRequestSubscribeChannelRemove(s)
	},

	// ChatSend - msgcli\chatsend.go
	"ChatSend": func(s string) (interface{}, error) {
		return msgcli.NewChatSend(s)
	},

	// ChatServerMessage - msgsvr\chatservermessage.go
	"ChatServerMessage": func(s string) (interface{}, error) {
		return msgsvr.NewChatServerMessage(s)
	},

	// ChatSmiley - msgsvr\chatsmiley.go
	"ChatSmiley": func(s string) (interface{}, error) {
		return msgsvr.NewChatSmiley(s)
	},

	// ChatSubscribeChannelAdd - msgsvr\chatsubscribechanneladd.go
	"ChatSubscribeChannelAdd": func(s string) (interface{}, error) {
		return msgsvr.NewChatSubscribeChannelAdd(s)
	},

	// ChatSubscribeChannelRemove - msgsvr\chatsubscribechannelremove.go
	"ChatSubscribeChannelRemove": func(s string) (interface{}, error) {
		return msgsvr.NewChatSubscribeChannelRemove(s)
	},

	// ChatUseSmiley - msgcli\chatusesmiley.go
	"ChatUseSmiley": func(s string) (interface{}, error) {
		return msgcli.NewChatUseSmiley(s)
	},

	// ConquestAreaAlignmentChanged - msgsvr\conquestareaalignmentchanged.go
	"ConquestAreaAlignmentChanged": func(s string) (interface{}, error) {
		return msgsvr.NewConquestAreaAlignmentChanged(s)
	},

	// ConquestConquestBalance - msgsvr\conquestconquestbalance.go
	"ConquestConquestBalance": func(s string) (interface{}, error) {
		return msgsvr.NewConquestConquestBalance(s)
	},

	// ConquestConquestBonus - msgsvr\conquestconquestbonus.go
	"ConquestConquestBonus": func(s string) (interface{}, error) {
		return msgsvr.NewConquestConquestBonus(s)
	},

	// ConquestGetAlignedBonus - msgcli\conquestgetalignedbonus.go
	"ConquestGetAlignedBonus": func(s string) (interface{}, error) {
		return msgcli.NewConquestGetAlignedBonus(s)
	},

	// ConquestPrismAttacked - msgsvr\conquestprismattacked.go
	"ConquestPrismAttacked": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismAttacked(s)
	},

	// ConquestPrismDead - msgsvr\conquestprismdead.go
	"ConquestPrismDead": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismDead(s)
	},

	// ConquestPrismFightAddEnemyAdd - msgsvr\conquestprismfightaddenemyadd.go
	"ConquestPrismFightAddEnemyAdd": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismFightAddEnemyAdd(s)
	},

	// ConquestPrismFightAddEnemyRemove - msgsvr\conquestprismfightaddenemyremove.go
	"ConquestPrismFightAddEnemyRemove": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismFightAddEnemyRemove(s)
	},

	// ConquestPrismFightAddPlayerAdd - msgsvr\conquestprismfightaddplayeradd.go
	"ConquestPrismFightAddPlayerAdd": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismFightAddPlayerAdd(s)
	},

	// ConquestPrismFightAddPlayerRemove - msgsvr\conquestprismfightaddplayerremove.go
	"ConquestPrismFightAddPlayerRemove": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismFightAddPlayerRemove(s)
	},

	// ConquestPrismFightJoin - msgcli\conquestprismfightjoin.go
	"ConquestPrismFightJoin": func(s string) (interface{}, error) {
		return msgcli.NewConquestPrismFightJoin(s)
	},

	// ConquestPrismFightLeave - msgcli\conquestprismfightleave.go
	"ConquestPrismFightLeave": func(s string) (interface{}, error) {
		return msgcli.NewConquestPrismFightLeave(s)
	},

	// ConquestPrismInfosClosing - msgsvr\conquestprisminfosclosing.go
	"ConquestPrismInfosClosing": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismInfosClosing(s)
	},

	// ConquestPrismInfosJoin - msgcli\conquestprisminfosjoin.go
	"ConquestPrismInfosJoin": func(s string) (interface{}, error) {
		return msgcli.NewConquestPrismInfosJoin(s)
	},

	// ConquestPrismInfosJoined - msgsvr\conquestprisminfosjoined.go
	"ConquestPrismInfosJoined": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismInfosJoined(s)
	},

	// ConquestPrismInfosLeave - msgcli\conquestprisminfosleave.go
	"ConquestPrismInfosLeave": func(s string) (interface{}, error) {
		return msgcli.NewConquestPrismInfosLeave(s)
	},

	// ConquestPrismSurvived - msgsvr\conquestprismsurvived.go
	"ConquestPrismSurvived": func(s string) (interface{}, error) {
		return msgsvr.NewConquestPrismSurvived(s)
	},

	// ConquestRequestBalance - msgcli\conquestrequestbalance.go
	"ConquestRequestBalance": func(s string) (interface{}, error) {
		return msgcli.NewConquestRequestBalance(s)
	},

	// ConquestSwitchPlaces - msgcli\conquestswitchplaces.go
	"ConquestSwitchPlaces": func(s string) (interface{}, error) {
		return msgcli.NewConquestSwitchPlaces(s)
	},

	// ConquestWorldData - msgsvr\conquestworlddata.go
	"ConquestWorldData": func(s string) (interface{}, error) {
		return msgsvr.NewConquestWorldData(s)
	},

	// ConquestWorldInfosJoin - msgcli\conquestworldinfosjoin.go
	"ConquestWorldInfosJoin": func(s string) (interface{}, error) {
		return msgcli.NewConquestWorldInfosJoin(s)
	},

	// ConquestWorldInfosLave - msgcli\conquestworldinfoslave.go
	"ConquestWorldInfosLave": func(s string) (interface{}, error) {
		return msgcli.NewConquestWorldInfosLave(s)
	},

	// DialogBeginning - msgcli\dialogbeginning.go
	"DialogBeginning": func(s string) (interface{}, error) {
		return msgcli.NewDialogBeginning(s)
	},

	// DialogCreate - msgcli\dialogcreate.go
	"DialogCreate": func(s string) (interface{}, error) {
		return msgcli.NewDialogCreate(s)
	},

	// DialogCreateError - msgsvr\dialogcreateerror.go
	"DialogCreateError": func(s string) (interface{}, error) {
		return msgsvr.NewDialogCreateError(s)
	},

	// DialogCreateSuccess - msgsvr\dialogcreatesuccess.go
	"DialogCreateSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewDialogCreateSuccess(s)
	},

	// DialogCustomAction - msgsvr\dialogcustomaction.go
	"DialogCustomAction": func(s string) (interface{}, error) {
		return msgsvr.NewDialogCustomAction(s)
	},

	// DialogLeave - msgsvr\dialogleave.go
	"DialogLeave": func(s string) (interface{}, error) {
		return msgsvr.NewDialogLeave(s)
	},

	// DialogPause - msgsvr\dialogpause.go
	"DialogPause": func(s string) (interface{}, error) {
		return msgsvr.NewDialogPause(s)
	},

	// DialogQuestion - msgsvr\dialogquestion.go
	"DialogQuestion": func(s string) (interface{}, error) {
		return msgsvr.NewDialogQuestion(s)
	},

	// DialogRequestLeave - msgcli\dialogrequestleave.go
	"DialogRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewDialogRequestLeave(s)
	},

	// DialogResponse - msgcli\dialogresponse.go
	"DialogResponse": func(s string) (interface{}, error) {
		return msgcli.NewDialogResponse(s)
	},

	// DocumentsCreateError - msgsvr\documentscreateerror.go
	"DocumentsCreateError": func(s string) (interface{}, error) {
		return msgsvr.NewDocumentsCreateError(s)
	},

	// DocumentsCreateSuccess - msgsvr\documentscreatesuccess.go
	"DocumentsCreateSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewDocumentsCreateSuccess(s)
	},

	// DocumentsLeave - msgsvr\documentsleave.go
	"DocumentsLeave": func(s string) (interface{}, error) {
		return msgsvr.NewDocumentsLeave(s)
	},

	// DocumentsRequestLeave - msgcli\documentsrequestleave.go
	"DocumentsRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewDocumentsRequestLeave(s)
	},

	// EmotesAdd - msgsvr\emotesadd.go
	"EmotesAdd": func(s string) (interface{}, error) {
		return msgsvr.NewEmotesAdd(s)
	},

	// EmotesDirection - msgsvr\emotesdirection.go
	"EmotesDirection": func(s string) (interface{}, error) {
		return msgsvr.NewEmotesDirection(s)
	},

	// EmotesList - msgsvr\emoteslist.go
	"EmotesList": func(s string) (interface{}, error) {
		return msgsvr.NewEmotesList(s)
	},

	// EmotesRemove - msgsvr\emotesremove.go
	"EmotesRemove": func(s string) (interface{}, error) {
		return msgsvr.NewEmotesRemove(s)
	},

	// EmotesSetDirection - msgcli\emotessetdirection.go
	"EmotesSetDirection": func(s string) (interface{}, error) {
		return msgcli.NewEmotesSetDirection(s)
	},

	// EmotesUseEmote - msgcli\emotesuseemote.go
	"EmotesUseEmote": func(s string) (interface{}, error) {
		return msgcli.NewEmotesUseEmote(s)
	},

	// EmotesUseError - msgsvr\emotesuseerror.go
	"EmotesUseError": func(s string) (interface{}, error) {
		return msgsvr.NewEmotesUseError(s)
	},

	// EmotesUseSuccess - msgsvr\emotesusesuccess.go
	"EmotesUseSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewEmotesUseSuccess(s)
	},

	// EnemiesAddEnemy - msgcli\enemiesaddenemy.go
	"EnemiesAddEnemy": func(s string) (interface{}, error) {
		return msgcli.NewEnemiesAddEnemy(s)
	},

	// EnemiesAddEnemyError - msgsvr\enemiesaddenemyerror.go
	"EnemiesAddEnemyError": func(s string) (interface{}, error) {
		return msgsvr.NewEnemiesAddEnemyError(s)
	},

	// EnemiesAddEnemySuccess - msgsvr\enemiesaddenemysuccess.go
	"EnemiesAddEnemySuccess": func(s string) (interface{}, error) {
		return msgsvr.NewEnemiesAddEnemySuccess(s)
	},

	// EnemiesEnemiesList - msgsvr\enemiesenemieslist.go
	"EnemiesEnemiesList": func(s string) (interface{}, error) {
		return msgsvr.NewEnemiesEnemiesList(s)
	},

	// EnemiesGetEnemiesList - msgcli\enemiesgetenemieslist.go
	"EnemiesGetEnemiesList": func(s string) (interface{}, error) {
		return msgcli.NewEnemiesGetEnemiesList(s)
	},

	// EnemiesRemoveEnemy - msgcli\enemiesremoveenemy.go
	"EnemiesRemoveEnemy": func(s string) (interface{}, error) {
		return msgcli.NewEnemiesRemoveEnemy(s)
	},

	// EnemiesRemoveEnemyError - msgsvr\enemiesremoveenemyerror.go
	"EnemiesRemoveEnemyError": func(s string) (interface{}, error) {
		return msgsvr.NewEnemiesRemoveEnemyError(s)
	},

	// EnemiesRemoveEnemySuccess - msgsvr\enemiesremoveenemysuccess.go
	"EnemiesRemoveEnemySuccess": func(s string) (interface{}, error) {
		return msgsvr.NewEnemiesRemoveEnemySuccess(s)
	},

	// ExchangeAccept - msgcli\exchangeaccept.go
	"ExchangeAccept": func(s string) (interface{}, error) {
		return msgcli.NewExchangeAccept(s)
	},

	// ExchangeAskOfflineExchange - msgsvr\exchangeaskofflineexchange.go
	"ExchangeAskOfflineExchange": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeAskOfflineExchange(s)
	},

	// ExchangeBigStoreBuy - msgcli\exchangebigstorebuy.go
	"ExchangeBigStoreBuy": func(s string) (interface{}, error) {
		return msgcli.NewExchangeBigStoreBuy(s)
	},

	// ExchangeBigStoreItemList - msgcli\exchangebigstoreitemlist.go
	"ExchangeBigStoreItemList": func(s string) (interface{}, error) {
		return msgcli.NewExchangeBigStoreItemList(s)
	},

	// ExchangeBigStoreItemMiddlePriceInBigStore - msgsvr\exchangebigstoreitemmiddlepriceinbigstore.go
	"ExchangeBigStoreItemMiddlePriceInBigStore": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBigStoreItemMiddlePriceInBigStore(s)
	},

	// ExchangeBigStoreItemsList - msgsvr\exchangebigstoreitemslist.go
	"ExchangeBigStoreItemsList": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBigStoreItemsList(s)
	},

	// ExchangeBigStoreItemsMovementAdd - msgsvr\exchangebigstoreitemsmovementadd.go
	"ExchangeBigStoreItemsMovementAdd": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBigStoreItemsMovementAdd(s)
	},

	// ExchangeBigStoreItemsMovementRemove - msgsvr\exchangebigstoreitemsmovementremove.go
	"ExchangeBigStoreItemsMovementRemove": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBigStoreItemsMovementRemove(s)
	},

	// ExchangeBigStoreSearch - msgcli\exchangebigstoresearch.go
	"ExchangeBigStoreSearch": func(s string) (interface{}, error) {
		return msgcli.NewExchangeBigStoreSearch(s)
	},

	// ExchangeBigStoreType - msgcli\exchangebigstoretype.go
	"ExchangeBigStoreType": func(s string) (interface{}, error) {
		return msgcli.NewExchangeBigStoreType(s)
	},

	// ExchangeBigStoreTypeItemsList - msgsvr\exchangebigstoretypeitemslist.go
	"ExchangeBigStoreTypeItemsList": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBigStoreTypeItemsList(s)
	},

	// ExchangeBigStoreTypeItemsMovementAdd - msgsvr\exchangebigstoretypeitemsmovementadd.go
	"ExchangeBigStoreTypeItemsMovementAdd": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBigStoreTypeItemsMovementAdd(s)
	},

	// ExchangeBigStoreTypeItemsMovementRemove - msgsvr\exchangebigstoretypeitemsmovementremove.go
	"ExchangeBigStoreTypeItemsMovementRemove": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBigStoreTypeItemsMovementRemove(s)
	},

	// ExchangeBuyError - msgsvr\exchangebuyerror.go
	"ExchangeBuyError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBuyError(s)
	},

	// ExchangeBuySuccess - msgsvr\exchangebuysuccess.go
	"ExchangeBuySuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeBuySuccess(s)
	},

	// ExchangeCoopMovementError - msgsvr\exchangecoopmovementerror.go
	"ExchangeCoopMovementError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCoopMovementError(s)
	},

	// ExchangeCoopMovementSuccess - msgsvr\exchangecoopmovementsuccess.go
	"ExchangeCoopMovementSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCoopMovementSuccess(s)
	},

	// ExchangeCraftError - msgsvr\exchangecrafterror.go
	"ExchangeCraftError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCraftError(s)
	},

	// ExchangeCraftLoop - msgsvr\exchangecraftloop.go
	"ExchangeCraftLoop": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCraftLoop(s)
	},

	// ExchangeCraftLoopEnd - msgsvr\exchangecraftloopend.go
	"ExchangeCraftLoopEnd": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCraftLoopEnd(s)
	},

	// ExchangeCraftPublicMode - msgsvr\exchangecraftpublicmode.go
	"ExchangeCraftPublicMode": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCraftPublicMode(s)
	},

	// ExchangeCraftSuccess - msgsvr\exchangecraftsuccess.go
	"ExchangeCraftSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCraftSuccess(s)
	},

	// ExchangeCrafterReferenceAdd - msgsvr\exchangecrafterreferenceadd.go
	"ExchangeCrafterReferenceAdd": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCrafterReferenceAdd(s)
	},

	// ExchangeCrafterReferenceRemove - msgsvr\exchangecrafterreferenceremove.go
	"ExchangeCrafterReferenceRemove": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCrafterReferenceRemove(s)
	},

	// ExchangeCreateError - msgsvr\exchangecreateerror.go
	"ExchangeCreateError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCreateError(s)
	},

	// ExchangeCreateSuccess - msgsvr\exchangecreatesuccess.go
	"ExchangeCreateSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeCreateSuccess(s)
	},

	// ExchangeGetCrafterForJob - msgcli\exchangegetcrafterforjob.go
	"ExchangeGetCrafterForJob": func(s string) (interface{}, error) {
		return msgcli.NewExchangeGetCrafterForJob(s)
	},

	// ExchangeGetItemMiddlePriceInBigStore - msgcli\exchangegetitemmiddlepriceinbigstore.go
	"ExchangeGetItemMiddlePriceInBigStore": func(s string) (interface{}, error) {
		return msgcli.NewExchangeGetItemMiddlePriceInBigStore(s)
	},

	// ExchangeKillMount - msgcli\exchangekillmount.go
	"ExchangeKillMount": func(s string) (interface{}, error) {
		return msgcli.NewExchangeKillMount(s)
	},

	// ExchangeKillMountInPark - msgcli\exchangekillmountinpark.go
	"ExchangeKillMountInPark": func(s string) (interface{}, error) {
		return msgcli.NewExchangeKillMountInPark(s)
	},

	// ExchangeLeave - msgcli\exchangeleave.go
	"ExchangeLeave": func(s string) (interface{}, error) {
		return msgcli.NewExchangeLeave(s)
	},

	// ExchangeLeaveError - msgsvr\exchangeleaveerror.go
	"ExchangeLeaveError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeLeaveError(s)
	},

	// ExchangeLeaveSuccess - msgsvr\exchangeleavesuccess.go
	"ExchangeLeaveSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeLeaveSuccess(s)
	},

	// ExchangeList - msgsvr\exchangelist.go
	"ExchangeList": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeList(s)
	},

	// ExchangeLocalDistantError - msgsvr\exchangelocaldistanterror.go
	"ExchangeLocalDistantError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeLocalDistantError(s)
	},

	// ExchangeLocalDistantSuccess - msgsvr\exchangelocaldistantsuccess.go
	"ExchangeLocalDistantSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeLocalDistantSuccess(s)
	},

	// ExchangeLocalMovementError - msgsvr\exchangelocalmovementerror.go
	"ExchangeLocalMovementError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeLocalMovementError(s)
	},

	// ExchangeLocalMovementSuccess - msgsvr\exchangelocalmovementsuccess.go
	"ExchangeLocalMovementSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeLocalMovementSuccess(s)
	},

	// ExchangeMountPark - msgsvr\exchangemountpark.go
	"ExchangeMountPark": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeMountPark(s)
	},

	// ExchangeMountPods - msgsvr\exchangemountpods.go
	"ExchangeMountPods": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeMountPods(s)
	},

	// ExchangeMountStorageAdd - msgsvr\exchangemountstorageadd.go
	"ExchangeMountStorageAdd": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeMountStorageAdd(s)
	},

	// ExchangeMountStorageRemove - msgsvr\exchangemountstorageremove.go
	"ExchangeMountStorageRemove": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeMountStorageRemove(s)
	},

	// ExchangeMovementBuy - msgcli\exchangemovementbuy.go
	"ExchangeMovementBuy": func(s string) (interface{}, error) {
		return msgcli.NewExchangeMovementBuy(s)
	},

	// ExchangeMovementItems - msgcli\exchangemovementitems.go
	"ExchangeMovementItems": func(s string) (interface{}, error) {
		return msgcli.NewExchangeMovementItems(s)
	},

	// ExchangeMovementKamas - msgcli\exchangemovementkamas.go
	"ExchangeMovementKamas": func(s string) (interface{}, error) {
		return msgcli.NewExchangeMovementKamas(s)
	},

	// ExchangeMovementPay - msgcli\exchangemovementpay.go
	"ExchangeMovementPay": func(s string) (interface{}, error) {
		return msgcli.NewExchangeMovementPay(s)
	},

	// ExchangeMovementSell - msgcli\exchangemovementsell.go
	"ExchangeMovementSell": func(s string) (interface{}, error) {
		return msgcli.NewExchangeMovementSell(s)
	},

	// ExchangeOfflineExchange - msgcli\exchangeofflineexchange.go
	"ExchangeOfflineExchange": func(s string) (interface{}, error) {
		return msgcli.NewExchangeOfflineExchange(s)
	},

	// ExchangePayMovementError - msgsvr\exchangepaymovementerror.go
	"ExchangePayMovementError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangePayMovementError(s)
	},

	// ExchangePayMovementSuccess - msgsvr\exchangepaymovementsuccess.go
	"ExchangePayMovementSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangePayMovementSuccess(s)
	},

	// ExchangePlayerShopMovementError - msgsvr\exchangeplayershopmovementerror.go
	"ExchangePlayerShopMovementError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangePlayerShopMovementError(s)
	},

	// ExchangePlayerShopMovementSuccess - msgsvr\exchangeplayershopmovementsuccess.go
	"ExchangePlayerShopMovementSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangePlayerShopMovementSuccess(s)
	},

	// ExchangePutInCertificateFromShed - msgcli\exchangeputincertificatefromshed.go
	"ExchangePutInCertificateFromShed": func(s string) (interface{}, error) {
		return msgcli.NewExchangePutInCertificateFromShed(s)
	},

	// ExchangePutInInventoryFromShed - msgcli\exchangeputininventoryfromshed.go
	"ExchangePutInInventoryFromShed": func(s string) (interface{}, error) {
		return msgcli.NewExchangePutInInventoryFromShed(s)
	},

	// ExchangePutInMountParkFromShed - msgcli\exchangeputinmountparkfromshed.go
	"ExchangePutInMountParkFromShed": func(s string) (interface{}, error) {
		return msgcli.NewExchangePutInMountParkFromShed(s)
	},

	// ExchangePutInShedFromCertificate - msgcli\exchangeputinshedfromcertificate.go
	"ExchangePutInShedFromCertificate": func(s string) (interface{}, error) {
		return msgcli.NewExchangePutInShedFromCertificate(s)
	},

	// ExchangePutInShedFromInventory - msgcli\exchangeputinshedfrominventory.go
	"ExchangePutInShedFromInventory": func(s string) (interface{}, error) {
		return msgcli.NewExchangePutInShedFromInventory(s)
	},

	// ExchangePutInShedFromMountPark - msgcli\exchangeputinshedfrommountpark.go
	"ExchangePutInShedFromMountPark": func(s string) (interface{}, error) {
		return msgcli.NewExchangePutInShedFromMountPark(s)
	},

	// ExchangeReady - msgsvr\exchangeready.go
	"ExchangeReady": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeReady(s)
	},

	// ExchangeRepeatCraft - msgcli\exchangerepeatcraft.go
	"ExchangeRepeatCraft": func(s string) (interface{}, error) {
		return msgcli.NewExchangeRepeatCraft(s)
	},

	// ExchangeReplayCraft - msgcli\exchangereplaycraft.go
	"ExchangeReplayCraft": func(s string) (interface{}, error) {
		return msgcli.NewExchangeReplayCraft(s)
	},

	// ExchangeRequest - msgcli\exchangerequest.go
	"ExchangeRequest": func(s string) (interface{}, error) {
		return msgcli.NewExchangeRequest(s)
	},

	// ExchangeRequestAskOfflineExchange - msgcli\exchangerequestaskofflineexchange.go
	"ExchangeRequestAskOfflineExchange": func(s string) (interface{}, error) {
		return msgcli.NewExchangeRequestAskOfflineExchange(s)
	},

	// ExchangeRequestError - msgsvr\exchangerequesterror.go
	"ExchangeRequestError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeRequestError(s)
	},

	// ExchangeRequestReady - msgcli\exchangerequestready.go
	"ExchangeRequestReady": func(s string) (interface{}, error) {
		return msgcli.NewExchangeRequestReady(s)
	},

	// ExchangeRequestSuccess - msgsvr\exchangerequestsuccess.go
	"ExchangeRequestSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeRequestSuccess(s)
	},

	// ExchangeSearchError - msgsvr\exchangesearcherror.go
	"ExchangeSearchError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeSearchError(s)
	},

	// ExchangeSearchSuccess - msgsvr\exchangesearchsuccess.go
	"ExchangeSearchSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeSearchSuccess(s)
	},

	// ExchangeSellError - msgsvr\exchangesellerror.go
	"ExchangeSellError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeSellError(s)
	},

	// ExchangeSellSuccess - msgsvr\exchangesellsuccess.go
	"ExchangeSellSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeSellSuccess(s)
	},

	// ExchangeSetPublicMode - msgcli\exchangesetpublicmode.go
	"ExchangeSetPublicMode": func(s string) (interface{}, error) {
		return msgcli.NewExchangeSetPublicMode(s)
	},

	// ExchangeShop - msgcli\exchangeshop.go
	"ExchangeShop": func(s string) (interface{}, error) {
		return msgcli.NewExchangeShop(s)
	},

	// ExchangeStopRepeatCraft - msgcli\exchangestoprepeatcraft.go
	"ExchangeStopRepeatCraft": func(s string) (interface{}, error) {
		return msgcli.NewExchangeStopRepeatCraft(s)
	},

	// ExchangeStorageMovementError - msgsvr\exchangestoragemovementerror.go
	"ExchangeStorageMovementError": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeStorageMovementError(s)
	},

	// ExchangeStorageMovementSuccess - msgsvr\exchangestoragemovementsuccess.go
	"ExchangeStorageMovementSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewExchangeStorageMovementSuccess(s)
	},

	// FightsBlockJoiner - msgcli\fightsblockjoiner.go
	"FightsBlockJoiner": func(s string) (interface{}, error) {
		return msgcli.NewFightsBlockJoiner(s)
	},

	// FightsBlockJoinerExceptParty - msgcli\fightsblockjoinerexceptparty.go
	"FightsBlockJoinerExceptParty": func(s string) (interface{}, error) {
		return msgcli.NewFightsBlockJoinerExceptParty(s)
	},

	// FightsBlockSpectators - msgcli\fightsblockspectators.go
	"FightsBlockSpectators": func(s string) (interface{}, error) {
		return msgcli.NewFightsBlockSpectators(s)
	},

	// FightsCount - msgsvr\fightscount.go
	"FightsCount": func(s string) (interface{}, error) {
		return msgsvr.NewFightsCount(s)
	},

	// FightsDetails - msgsvr\fightsdetails.go
	"FightsDetails": func(s string) (interface{}, error) {
		return msgsvr.NewFightsDetails(s)
	},

	// FightsGetDetails - msgcli\fightsgetdetails.go
	"FightsGetDetails": func(s string) (interface{}, error) {
		return msgcli.NewFightsGetDetails(s)
	},

	// FightsGetList - msgcli\fightsgetlist.go
	"FightsGetList": func(s string) (interface{}, error) {
		return msgcli.NewFightsGetList(s)
	},

	// FightsList - msgsvr\fightslist.go
	"FightsList": func(s string) (interface{}, error) {
		return msgsvr.NewFightsList(s)
	},

	// FightsNeedHelp - msgcli\fightsneedhelp.go
	"FightsNeedHelp": func(s string) (interface{}, error) {
		return msgcli.NewFightsNeedHelp(s)
	},

	// FriendsAddFriend - msgcli\friendsaddfriend.go
	"FriendsAddFriend": func(s string) (interface{}, error) {
		return msgcli.NewFriendsAddFriend(s)
	},

	// FriendsAddFriendError - msgsvr\friendsaddfrienderror.go
	"FriendsAddFriendError": func(s string) (interface{}, error) {
		return msgsvr.NewFriendsAddFriendError(s)
	},

	// FriendsAddFriendSuccess - msgsvr\friendsaddfriendsuccess.go
	"FriendsAddFriendSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewFriendsAddFriendSuccess(s)
	},

	// FriendsCompass - msgcli\friendscompass.go
	"FriendsCompass": func(s string) (interface{}, error) {
		return msgcli.NewFriendsCompass(s)
	},

	// FriendsFriendsList - msgsvr\friendsfriendslist.go
	"FriendsFriendsList": func(s string) (interface{}, error) {
		return msgsvr.NewFriendsFriendsList(s)
	},

	// FriendsGetFriendsList - msgcli\friendsgetfriendslist.go
	"FriendsGetFriendsList": func(s string) (interface{}, error) {
		return msgcli.NewFriendsGetFriendsList(s)
	},

	// FriendsJoin - msgcli\friendsjoin.go
	"FriendsJoin": func(s string) (interface{}, error) {
		return msgcli.NewFriendsJoin(s)
	},

	// FriendsJoinFriend - msgcli\friendsjoinfriend.go
	"FriendsJoinFriend": func(s string) (interface{}, error) {
		return msgcli.NewFriendsJoinFriend(s)
	},

	// FriendsNotifyChange - msgsvr\friendsnotifychange.go
	"FriendsNotifyChange": func(s string) (interface{}, error) {
		return msgsvr.NewFriendsNotifyChange(s)
	},

	// FriendsRemoveFriend - msgcli\friendsremovefriend.go
	"FriendsRemoveFriend": func(s string) (interface{}, error) {
		return msgcli.NewFriendsRemoveFriend(s)
	},

	// FriendsRemoveFriendError - msgsvr\friendsremovefrienderror.go
	"FriendsRemoveFriendError": func(s string) (interface{}, error) {
		return msgsvr.NewFriendsRemoveFriendError(s)
	},

	// FriendsRemoveFriendSuccess - msgsvr\friendsremovefriendsuccess.go
	"FriendsRemoveFriendSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewFriendsRemoveFriendSuccess(s)
	},

	// FriendsSetNotifyWhenConnect - msgcli\friendssetnotifywhenconnect.go
	"FriendsSetNotifyWhenConnect": func(s string) (interface{}, error) {
		return msgcli.NewFriendsSetNotifyWhenConnect(s)
	},

	// FriendsSpouse - msgsvr\friendsspouse.go
	"FriendsSpouse": func(s string) (interface{}, error) {
		return msgsvr.NewFriendsSpouse(s)
	},

	// GameActionAck - msgcli\gameactionack.go
	"GameActionAck": func(s string) (interface{}, error) {
		return msgcli.NewGameActionAck(s)
	},

	// GameActionCancel - msgcli\gameactioncancel.go
	"GameActionCancel": func(s string) (interface{}, error) {
		return msgcli.NewGameActionCancel(s)
	},

	// GameActions - msgsvr\gameactions.go
	"GameActions": func(s string) (interface{}, error) {
		return msgsvr.NewGameActions(s)
	},

	// GameActionsFinish - msgsvr\gameactionsfinish.go
	"GameActionsFinish": func(s string) (interface{}, error) {
		return msgsvr.NewGameActionsFinish(s)
	},

	// GameActionsSendActions - msgcli\gameactionssendactions.go
	"GameActionsSendActions": func(s string) (interface{}, error) {
		return msgcli.NewGameActionsSendActions(s)
	},

	// GameActionsStart - msgsvr\gameactionsstart.go
	"GameActionsStart": func(s string) (interface{}, error) {
		return msgsvr.NewGameActionsStart(s)
	},

	// GameAskDisablePVPMode - msgcli\gameaskdisablepvpmode.go
	"GameAskDisablePVPMode": func(s string) (interface{}, error) {
		return msgcli.NewGameAskDisablePVPMode(s)
	},

	// GameCellData - msgsvr\gamecelldata.go
	"GameCellData": func(s string) (interface{}, error) {
		return msgsvr.NewGameCellData(s)
	},

	// GameCellObject - msgsvr\gamecellobject.go
	"GameCellObject": func(s string) (interface{}, error) {
		return msgsvr.NewGameCellObject(s)
	},

	// GameChallenge - msgsvr\gamechallenge.go
	"GameChallenge": func(s string) (interface{}, error) {
		return msgsvr.NewGameChallenge(s)
	},

	// GameClearAllEffect - msgsvr\gameclearalleffect.go
	"GameClearAllEffect": func(s string) (interface{}, error) {
		return msgsvr.NewGameClearAllEffect(s)
	},

	// GameCreate - msgcli\gamecreate.go
	"GameCreate": func(s string) (interface{}, error) {
		return msgcli.NewGameCreate(s)
	},

	// GameCreateError - msgsvr\gamecreateerror.go
	"GameCreateError": func(s string) (interface{}, error) {
		return msgsvr.NewGameCreateError(s)
	},

	// GameCreateSuccess - msgsvr\gamecreatesuccess.go
	"GameCreateSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewGameCreateSuccess(s)
	},

	// GameEffect - msgsvr\gameeffect.go
	"GameEffect": func(s string) (interface{}, error) {
		return msgsvr.NewGameEffect(s)
	},

	// GameEnabledPVPMode - msgcli\gameenabledpvpmode.go
	"GameEnabledPVPMode": func(s string) (interface{}, error) {
		return msgcli.NewGameEnabledPVPMode(s)
	},

	// GameEnd - msgsvr\gameend.go
	"GameEnd": func(s string) (interface{}, error) {
		return msgsvr.NewGameEnd(s)
	},

	// GameExtraClip - msgsvr\gameextraclip.go
	"GameExtraClip": func(s string) (interface{}, error) {
		return msgsvr.NewGameExtraClip(s)
	},

	// GameFightChallenge - msgsvr\gamefightchallenge.go
	"GameFightChallenge": func(s string) (interface{}, error) {
		return msgsvr.NewGameFightChallenge(s)
	},

	// GameFightChallengeUpdateError - msgsvr\gamefightchallengeupdateerror.go
	"GameFightChallengeUpdateError": func(s string) (interface{}, error) {
		return msgsvr.NewGameFightChallengeUpdateError(s)
	},

	// GameFightChallengeUpdateSuccess - msgsvr\gamefightchallengeupdatesuccess.go
	"GameFightChallengeUpdateSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewGameFightChallengeUpdateSuccess(s)
	},

	// GameFightOption - msgsvr\gamefightoption.go
	"GameFightOption": func(s string) (interface{}, error) {
		return msgsvr.NewGameFightOption(s)
	},

	// GameFlag - msgsvr\gameflag.go
	"GameFlag": func(s string) (interface{}, error) {
		return msgsvr.NewGameFlag(s)
	},

	// GameFrameObject2 - msgsvr\gameframeobject2.go
	"GameFrameObject2": func(s string) (interface{}, error) {
		return msgsvr.NewGameFrameObject2(s)
	},

	// GameFrameObjectExternal - msgsvr\gameframeobjectexternal.go
	"GameFrameObjectExternal": func(s string) (interface{}, error) {
		return msgsvr.NewGameFrameObjectExternal(s)
	},

	// GameFreeMySoul - msgcli\gamefreemysoul.go
	"GameFreeMySoul": func(s string) (interface{}, error) {
		return msgcli.NewGameFreeMySoul(s)
	},

	// GameGameOver - msgsvr\gamegameover.go
	"GameGameOver": func(s string) (interface{}, error) {
		return msgsvr.NewGameGameOver(s)
	},

	// GameGetExtraInformations - msgcli\gamegetextrainformations.go
	"GameGetExtraInformations": func(s string) (interface{}, error) {
		return msgcli.NewGameGetExtraInformations(s)
	},

	// GameGetMapData - msgcli\gamegetmapdata.go
	"GameGetMapData": func(s string) (interface{}, error) {
		return msgcli.NewGameGetMapData(s)
	},

	// GameJoin - msgsvr\gamejoin.go
	"GameJoin": func(s string) (interface{}, error) {
		return msgsvr.NewGameJoin(s)
	},

	// GameLeave - msgsvr\gameleave.go
	"GameLeave": func(s string) (interface{}, error) {
		return msgsvr.NewGameLeave(s)
	},

	// GameMapData - msgsvr\gamemapdata.go
	"GameMapData": func(s string) (interface{}, error) {
		return msgsvr.NewGameMapData(s)
	},

	// GameMapLoaded - msgsvr\gamemaploaded.go
	"GameMapLoaded": func(s string) (interface{}, error) {
		return msgsvr.NewGameMapLoaded(s)
	},

	// GameMovement - msgsvr\gamemovement.go
	"GameMovement": func(s string) (interface{}, error) {
		return msgsvr.NewGameMovement(s)
	},

	// GameMovementRemove - msgsvr\gamemovementremove.go
	"GameMovementRemove": func(s string) (interface{}, error) {
		return msgsvr.NewGameMovementRemove(s)
	},

	// GamePVP - msgsvr\gamepvp.go
	"GamePVP": func(s string) (interface{}, error) {
		return msgsvr.NewGamePVP(s)
	},

	// GamePlayersCoordinates - msgsvr\gameplayerscoordinates.go
	"GamePlayersCoordinates": func(s string) (interface{}, error) {
		return msgsvr.NewGamePlayersCoordinates(s)
	},

	// GamePositionStart - msgsvr\gamepositionstart.go
	"GamePositionStart": func(s string) (interface{}, error) {
		return msgsvr.NewGamePositionStart(s)
	},

	// GameReady - msgsvr\gameready.go
	"GameReady": func(s string) (interface{}, error) {
		return msgsvr.NewGameReady(s)
	},

	// GameRequestLeave - msgcli\gamerequestleave.go
	"GameRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewGameRequestLeave(s)
	},

	// GameRequestReady - msgcli\gamerequestready.go
	"GameRequestReady": func(s string) (interface{}, error) {
		return msgcli.NewGameRequestReady(s)
	},

	// GameSetFlag - msgcli\gamesetflag.go
	"GameSetFlag": func(s string) (interface{}, error) {
		return msgcli.NewGameSetFlag(s)
	},

	// GameSetPlayerPosition - msgcli\gamesetplayerposition.go
	"GameSetPlayerPosition": func(s string) (interface{}, error) {
		return msgcli.NewGameSetPlayerPosition(s)
	},

	// GameShowFightChallengeTarget - msgcli\gameshowfightchallengetarget.go
	"GameShowFightChallengeTarget": func(s string) (interface{}, error) {
		return msgcli.NewGameShowFightChallengeTarget(s)
	},

	// GameStartToPlay - msgsvr\gamestarttoplay.go
	"GameStartToPlay": func(s string) (interface{}, error) {
		return msgsvr.NewGameStartToPlay(s)
	},

	// GameTeam - msgsvr\gameteam.go
	"GameTeam": func(s string) (interface{}, error) {
		return msgsvr.NewGameTeam(s)
	},

	// GameTurnEnd - msgcli\gameturnend.go
	"GameTurnEnd": func(s string) (interface{}, error) {
		return msgcli.NewGameTurnEnd(s)
	},

	// GameTurnFinish - msgsvr\gameturnfinish.go
	"GameTurnFinish": func(s string) (interface{}, error) {
		return msgsvr.NewGameTurnFinish(s)
	},

	// GameTurnList - msgsvr\gameturnlist.go
	"GameTurnList": func(s string) (interface{}, error) {
		return msgsvr.NewGameTurnList(s)
	},

	// GameTurnMiddle - msgsvr\gameturnmiddle.go
	"GameTurnMiddle": func(s string) (interface{}, error) {
		return msgsvr.NewGameTurnMiddle(s)
	},

	// GameTurnOk - msgcli\gameturnok.go
	"GameTurnOk": func(s string) (interface{}, error) {
		return msgcli.NewGameTurnOk(s)
	},

	// GameTurnReady - msgsvr\gameturnready.go
	"GameTurnReady": func(s string) (interface{}, error) {
		return msgsvr.NewGameTurnReady(s)
	},

	// GameTurnStart - msgsvr\gameturnstart.go
	"GameTurnStart": func(s string) (interface{}, error) {
		return msgsvr.NewGameTurnStart(s)
	},

	// GameZoneData - msgsvr\gamezonedata.go
	"GameZoneData": func(s string) (interface{}, error) {
		return msgsvr.NewGameZoneData(s)
	},

	// GildBanError - msgsvr\gildbanerror.go
	"GildBanError": func(s string) (interface{}, error) {
		return msgsvr.NewGildBanError(s)
	},

	// GildBanSuccess - msgsvr\gildbansuccess.go
	"GildBanSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewGildBanSuccess(s)
	},

	// GildHireTaxCollectorError - msgsvr\gildhiretaxcollectorerror.go
	"GildHireTaxCollectorError": func(s string) (interface{}, error) {
		return msgsvr.NewGildHireTaxCollectorError(s)
	},

	// GildHireTaxCollectorSuccess - msgsvr\gildhiretaxcollectorsuccess.go
	"GildHireTaxCollectorSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewGildHireTaxCollectorSuccess(s)
	},

	// GildTaxCollectorAttacked - msgsvr\gildtaxcollectorattacked.go
	"GildTaxCollectorAttacked": func(s string) (interface{}, error) {
		return msgsvr.NewGildTaxCollectorAttacked(s)
	},

	// GildTaxCollectorInfo - msgsvr\gildtaxcollectorinfo.go
	"GildTaxCollectorInfo": func(s string) (interface{}, error) {
		return msgsvr.NewGildTaxCollectorInfo(s)
	},

	// GildUserInterfaceOpen - msgsvr\gilduserinterfaceopen.go
	"GildUserInterfaceOpen": func(s string) (interface{}, error) {
		return msgsvr.NewGildUserInterfaceOpen(s)
	},

	// GuildAcceptInvitation - msgcli\guildacceptinvitation.go
	"GuildAcceptInvitation": func(s string) (interface{}, error) {
		return msgcli.NewGuildAcceptInvitation(s)
	},

	// GuildBan - msgcli\guildban.go
	"GuildBan": func(s string) (interface{}, error) {
		return msgcli.NewGuildBan(s)
	},

	// GuildBoostCharacteristic - msgcli\guildboostcharacteristic.go
	"GuildBoostCharacteristic": func(s string) (interface{}, error) {
		return msgcli.NewGuildBoostCharacteristic(s)
	},

	// GuildBoostSpell - msgcli\guildboostspell.go
	"GuildBoostSpell": func(s string) (interface{}, error) {
		return msgcli.NewGuildBoostSpell(s)
	},

	// GuildChangeMemberProfile - msgcli\guildchangememberprofile.go
	"GuildChangeMemberProfile": func(s string) (interface{}, error) {
		return msgcli.NewGuildChangeMemberProfile(s)
	},

	// GuildCreate - msgcli\guildcreate.go
	"GuildCreate": func(s string) (interface{}, error) {
		return msgcli.NewGuildCreate(s)
	},

	// GuildCreateError - msgsvr\guildcreateerror.go
	"GuildCreateError": func(s string) (interface{}, error) {
		return msgsvr.NewGuildCreateError(s)
	},

	// GuildCreateSuccess - msgsvr\guildcreatesuccess.go
	"GuildCreateSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewGuildCreateSuccess(s)
	},

	// GuildGetInfosBoosts - msgcli\guildgetinfosboosts.go
	"GuildGetInfosBoosts": func(s string) (interface{}, error) {
		return msgcli.NewGuildGetInfosBoosts(s)
	},

	// GuildGetInfosGeneral - msgcli\guildgetinfosgeneral.go
	"GuildGetInfosGeneral": func(s string) (interface{}, error) {
		return msgcli.NewGuildGetInfosGeneral(s)
	},

	// GuildGetInfosGuildHouses - msgcli\guildgetinfosguildhouses.go
	"GuildGetInfosGuildHouses": func(s string) (interface{}, error) {
		return msgcli.NewGuildGetInfosGuildHouses(s)
	},

	// GuildGetInfosMembers - msgcli\guildgetinfosmembers.go
	"GuildGetInfosMembers": func(s string) (interface{}, error) {
		return msgcli.NewGuildGetInfosMembers(s)
	},

	// GuildGetInfosMountPark - msgcli\guildgetinfosmountpark.go
	"GuildGetInfosMountPark": func(s string) (interface{}, error) {
		return msgcli.NewGuildGetInfosMountPark(s)
	},

	// GuildGetInfosTaxCollector - msgcli\guildgetinfostaxcollector.go
	"GuildGetInfosTaxCollector": func(s string) (interface{}, error) {
		return msgcli.NewGuildGetInfosTaxCollector(s)
	},

	// GuildHireTaxCollector - msgcli\guildhiretaxcollector.go
	"GuildHireTaxCollector": func(s string) (interface{}, error) {
		return msgcli.NewGuildHireTaxCollector(s)
	},

	// GuildInfosBoosts - msgsvr\guildinfosboosts.go
	"GuildInfosBoosts": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosBoosts(s)
	},

	// GuildInfosGeneral - msgsvr\guildinfosgeneral.go
	"GuildInfosGeneral": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosGeneral(s)
	},

	// GuildInfosHouses - msgsvr\guildinfoshouses.go
	"GuildInfosHouses": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosHouses(s)
	},

	// GuildInfosMembers - msgsvr\guildinfosmembers.go
	"GuildInfosMembers": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosMembers(s)
	},

	// GuildInfosMountPark - msgsvr\guildinfosmountpark.go
	"GuildInfosMountPark": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosMountPark(s)
	},

	// GuildInfosTaxCollectorsAttackers - msgsvr\guildinfostaxcollectorsattackers.go
	"GuildInfosTaxCollectorsAttackers": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosTaxCollectorsAttackers(s)
	},

	// GuildInfosTaxCollectorsMovement - msgsvr\guildinfostaxcollectorsmovement.go
	"GuildInfosTaxCollectorsMovement": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosTaxCollectorsMovement(s)
	},

	// GuildInfosTaxCollectorsPlayers - msgsvr\guildinfostaxcollectorsplayers.go
	"GuildInfosTaxCollectorsPlayers": func(s string) (interface{}, error) {
		return msgsvr.NewGuildInfosTaxCollectorsPlayers(s)
	},

	// GuildInvite - msgcli\guildinvite.go
	"GuildInvite": func(s string) (interface{}, error) {
		return msgcli.NewGuildInvite(s)
	},

	// GuildJoinDistantSuccess - msgsvr\guildjoindistantsuccess.go
	"GuildJoinDistantSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewGuildJoinDistantSuccess(s)
	},

	// GuildJoinError - msgsvr\guildjoinerror.go
	"GuildJoinError": func(s string) (interface{}, error) {
		return msgsvr.NewGuildJoinError(s)
	},

	// GuildJoinSuccess - msgsvr\guildjoinsuccess.go
	"GuildJoinSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewGuildJoinSuccess(s)
	},

	// GuildJoinTaxCollector - msgcli\guildjointaxcollector.go
	"GuildJoinTaxCollector": func(s string) (interface{}, error) {
		return msgcli.NewGuildJoinTaxCollector(s)
	},

	// GuildLeave - msgsvr\guildleave.go
	"GuildLeave": func(s string) (interface{}, error) {
		return msgsvr.NewGuildLeave(s)
	},

	// GuildLeaveTaxCollector - msgcli\guildleavetaxcollector.go
	"GuildLeaveTaxCollector": func(s string) (interface{}, error) {
		return msgcli.NewGuildLeaveTaxCollector(s)
	},

	// GuildLeaveTaxInterface - msgcli\guildleavetaxinterface.go
	"GuildLeaveTaxInterface": func(s string) (interface{}, error) {
		return msgcli.NewGuildLeaveTaxInterface(s)
	},

	// GuildNew - msgsvr\guildnew.go
	"GuildNew": func(s string) (interface{}, error) {
		return msgsvr.NewGuildNew(s)
	},

	// GuildRefuseInvitation - msgcli\guildrefuseinvitation.go
	"GuildRefuseInvitation": func(s string) (interface{}, error) {
		return msgcli.NewGuildRefuseInvitation(s)
	},

	// GuildRemoveTaxCollector - msgcli\guildremovetaxcollector.go
	"GuildRemoveTaxCollector": func(s string) (interface{}, error) {
		return msgcli.NewGuildRemoveTaxCollector(s)
	},

	// GuildRequestDistant - msgsvr\guildrequestdistant.go
	"GuildRequestDistant": func(s string) (interface{}, error) {
		return msgsvr.NewGuildRequestDistant(s)
	},

	// GuildRequestLeave - msgcli\guildrequestleave.go
	"GuildRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewGuildRequestLeave(s)
	},

	// GuildRequestLocal - msgsvr\guildrequestlocal.go
	"GuildRequestLocal": func(s string) (interface{}, error) {
		return msgsvr.NewGuildRequestLocal(s)
	},

	// GuildStats - msgsvr\guildstats.go
	"GuildStats": func(s string) (interface{}, error) {
		return msgsvr.NewGuildStats(s)
	},

	// GuildTeleportToGuildFarm - msgcli\guildteleporttoguildfarm.go
	"GuildTeleportToGuildFarm": func(s string) (interface{}, error) {
		return msgcli.NewGuildTeleportToGuildFarm(s)
	},

	// GuildTeleportToGuildHouse - msgcli\guildteleporttoguildhouse.go
	"GuildTeleportToGuildHouse": func(s string) (interface{}, error) {
		return msgcli.NewGuildTeleportToGuildHouse(s)
	},

	// HousesBuy - msgcli\housesbuy.go
	"HousesBuy": func(s string) (interface{}, error) {
		return msgcli.NewHousesBuy(s)
	},

	// HousesBuyError - msgsvr\housesbuyerror.go
	"HousesBuyError": func(s string) (interface{}, error) {
		return msgsvr.NewHousesBuyError(s)
	},

	// HousesBuySuccess - msgsvr\housesbuysuccess.go
	"HousesBuySuccess": func(s string) (interface{}, error) {
		return msgsvr.NewHousesBuySuccess(s)
	},

	// HousesCreate - msgsvr\housescreate.go
	"HousesCreate": func(s string) (interface{}, error) {
		return msgsvr.NewHousesCreate(s)
	},

	// HousesGuildInfos - msgsvr\housesguildinfos.go
	"HousesGuildInfos": func(s string) (interface{}, error) {
		return msgsvr.NewHousesGuildInfos(s)
	},

	// HousesKick - msgcli\houseskick.go
	"HousesKick": func(s string) (interface{}, error) {
		return msgcli.NewHousesKick(s)
	},

	// HousesLeave - msgsvr\housesleave.go
	"HousesLeave": func(s string) (interface{}, error) {
		return msgsvr.NewHousesLeave(s)
	},

	// HousesListAdd - msgsvr\houseslistadd.go
	"HousesListAdd": func(s string) (interface{}, error) {
		return msgsvr.NewHousesListAdd(s)
	},

	// HousesListRemove - msgsvr\houseslistremove.go
	"HousesListRemove": func(s string) (interface{}, error) {
		return msgsvr.NewHousesListRemove(s)
	},

	// HousesLockedProperty - msgsvr\houseslockedproperty.go
	"HousesLockedProperty": func(s string) (interface{}, error) {
		return msgsvr.NewHousesLockedProperty(s)
	},

	// HousesProperties - msgsvr\housesproperties.go
	"HousesProperties": func(s string) (interface{}, error) {
		return msgsvr.NewHousesProperties(s)
	},

	// HousesRequestLeave - msgcli\housesrequestleave.go
	"HousesRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewHousesRequestLeave(s)
	},

	// HousesSell - msgcli\housessell.go
	"HousesSell": func(s string) (interface{}, error) {
		return msgcli.NewHousesSell(s)
	},

	// HousesSellError - msgsvr\housessellerror.go
	"HousesSellError": func(s string) (interface{}, error) {
		return msgsvr.NewHousesSellError(s)
	},

	// HousesSellSuccess - msgsvr\housessellsuccess.go
	"HousesSellSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewHousesSellSuccess(s)
	},

	// HousesShare - msgcli\housesshare.go
	"HousesShare": func(s string) (interface{}, error) {
		return msgcli.NewHousesShare(s)
	},

	// HousesState - msgcli\housesstate.go
	"HousesState": func(s string) (interface{}, error) {
		return msgcli.NewHousesState(s)
	},

	// HousesUnShare - msgcli\housesunshare.go
	"HousesUnShare": func(s string) (interface{}, error) {
		return msgcli.NewHousesUnShare(s)
	},

	// InfosCompass - msgsvr\infoscompass.go
	"InfosCompass": func(s string) (interface{}, error) {
		return msgsvr.NewInfosCompass(s)
	},

	// InfosGetMaps - msgcli\infosgetmaps.go
	"InfosGetMaps": func(s string) (interface{}, error) {
		return msgcli.NewInfosGetMaps(s)
	},

	// InfosInfoCoordinatesPHighlight - msgsvr\infosinfocoordinatesphighlight.go
	"InfosInfoCoordinatesPHighlight": func(s string) (interface{}, error) {
		return msgsvr.NewInfosInfoCoordinatesPHighlight(s)
	},

	// InfosInfoMaps - msgsvr\infosinfomaps.go
	"InfosInfoMaps": func(s string) (interface{}, error) {
		return msgsvr.NewInfosInfoMaps(s)
	},

	// InfosLifeRestoreTimerFinish - msgsvr\infosliferestoretimerfinish.go
	"InfosLifeRestoreTimerFinish": func(s string) (interface{}, error) {
		return msgsvr.NewInfosLifeRestoreTimerFinish(s)
	},

	// InfosLifeRestoreTimerStart - msgsvr\infosliferestoretimerstart.go
	"InfosLifeRestoreTimerStart": func(s string) (interface{}, error) {
		return msgsvr.NewInfosLifeRestoreTimerStart(s)
	},

	// InfosMessage - msgsvr\infosmessage.go
	"InfosMessage": func(s string) (interface{}, error) {
		return msgsvr.NewInfosMessage(s)
	},

	// InfosQuantity - msgsvr\infosquantity.go
	"InfosQuantity": func(s string) (interface{}, error) {
		return msgsvr.NewInfosQuantity(s)
	},

	// InfosSendScreenInfo - msgcli\infossendscreeninfo.go
	"InfosSendScreenInfo": func(s string) (interface{}, error) {
		return msgcli.NewInfosSendScreenInfo(s)
	},

	// ItemsAccessories - msgsvr\itemsaccessories.go
	"ItemsAccessories": func(s string) (interface{}, error) {
		return msgsvr.NewItemsAccessories(s)
	},

	// ItemsAddError - msgsvr\itemsadderror.go
	"ItemsAddError": func(s string) (interface{}, error) {
		return msgsvr.NewItemsAddError(s)
	},

	// ItemsAddSuccess - msgsvr\itemsaddsuccess.go
	"ItemsAddSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewItemsAddSuccess(s)
	},

	// ItemsChange - msgsvr\itemschange.go
	"ItemsChange": func(s string) (interface{}, error) {
		return msgsvr.NewItemsChange(s)
	},

	// ItemsDestroy - msgcli\itemsdestroy.go
	"ItemsDestroy": func(s string) (interface{}, error) {
		return msgcli.NewItemsDestroy(s)
	},

	// ItemsDissociate - msgcli\itemsdissociate.go
	"ItemsDissociate": func(s string) (interface{}, error) {
		return msgcli.NewItemsDissociate(s)
	},

	// ItemsDrop - msgcli\itemsdrop.go
	"ItemsDrop": func(s string) (interface{}, error) {
		return msgcli.NewItemsDrop(s)
	},

	// ItemsDropError - msgsvr\itemsdroperror.go
	"ItemsDropError": func(s string) (interface{}, error) {
		return msgsvr.NewItemsDropError(s)
	},

	// ItemsDropSuccess - msgsvr\itemsdropsuccess.go
	"ItemsDropSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewItemsDropSuccess(s)
	},

	// ItemsFeed - msgcli\itemsfeed.go
	"ItemsFeed": func(s string) (interface{}, error) {
		return msgcli.NewItemsFeed(s)
	},

	// ItemsItemFound - msgsvr\itemsitemfound.go
	"ItemsItemFound": func(s string) (interface{}, error) {
		return msgsvr.NewItemsItemFound(s)
	},

	// ItemsItemSetAdd - msgsvr\itemsitemsetadd.go
	"ItemsItemSetAdd": func(s string) (interface{}, error) {
		return msgsvr.NewItemsItemSetAdd(s)
	},

	// ItemsItemSetRemove - msgsvr\itemsitemsetremove.go
	"ItemsItemSetRemove": func(s string) (interface{}, error) {
		return msgsvr.NewItemsItemSetRemove(s)
	},

	// ItemsItemUseCondition - msgsvr\itemsitemusecondition.go
	"ItemsItemUseCondition": func(s string) (interface{}, error) {
		return msgsvr.NewItemsItemUseCondition(s)
	},

	// ItemsMovement - msgsvr\itemsmovement.go
	"ItemsMovement": func(s string) (interface{}, error) {
		return msgsvr.NewItemsMovement(s)
	},

	// ItemsQuantity - msgsvr\itemsquantity.go
	"ItemsQuantity": func(s string) (interface{}, error) {
		return msgsvr.NewItemsQuantity(s)
	},

	// ItemsRemove - msgsvr\itemsremove.go
	"ItemsRemove": func(s string) (interface{}, error) {
		return msgsvr.NewItemsRemove(s)
	},

	// ItemsRequestMovement - msgcli\itemsrequestmovement.go
	"ItemsRequestMovement": func(s string) (interface{}, error) {
		return msgcli.NewItemsRequestMovement(s)
	},

	// ItemsSetSkin - msgcli\itemssetskin.go
	"ItemsSetSkin": func(s string) (interface{}, error) {
		return msgcli.NewItemsSetSkin(s)
	},

	// ItemsTool - msgsvr\itemstool.go
	"ItemsTool": func(s string) (interface{}, error) {
		return msgsvr.NewItemsTool(s)
	},

	// ItemsUseConfirm - msgcli\itemsuseconfirm.go
	"ItemsUseConfirm": func(s string) (interface{}, error) {
		return msgcli.NewItemsUseConfirm(s)
	},

	// ItemsUseNoConfirm - msgcli\itemsusenoconfirm.go
	"ItemsUseNoConfirm": func(s string) (interface{}, error) {
		return msgcli.NewItemsUseNoConfirm(s)
	},

	// ItemsWeight - msgsvr\itemsweight.go
	"ItemsWeight": func(s string) (interface{}, error) {
		return msgsvr.NewItemsWeight(s)
	},

	// JobChangeJobStats - msgcli\jobchangejobstats.go
	"JobChangeJobStats": func(s string) (interface{}, error) {
		return msgcli.NewJobChangeJobStats(s)
	},

	// JobLevel - msgsvr\joblevel.go
	"JobLevel": func(s string) (interface{}, error) {
		return msgsvr.NewJobLevel(s)
	},

	// JobOptions - msgsvr\joboptions.go
	"JobOptions": func(s string) (interface{}, error) {
		return msgsvr.NewJobOptions(s)
	},

	// JobRemove - msgsvr\jobremove.go
	"JobRemove": func(s string) (interface{}, error) {
		return msgsvr.NewJobRemove(s)
	},

	// JobSkills - msgsvr\jobskills.go
	"JobSkills": func(s string) (interface{}, error) {
		return msgsvr.NewJobSkills(s)
	},

	// JobXP - msgsvr\jobxp.go
	"JobXP": func(s string) (interface{}, error) {
		return msgsvr.NewJobXP(s)
	},

	// KeyCreate - msgsvr\keycreate.go
	"KeyCreate": func(s string) (interface{}, error) {
		return msgsvr.NewKeyCreate(s)
	},

	// KeyKeyError - msgsvr\keykeyerror.go
	"KeyKeyError": func(s string) (interface{}, error) {
		return msgsvr.NewKeyKeyError(s)
	},

	// KeyKeySuccess - msgsvr\keykeysuccess.go
	"KeyKeySuccess": func(s string) (interface{}, error) {
		return msgsvr.NewKeyKeySuccess(s)
	},

	// KeyLeave - msgsvr\keyleave.go
	"KeyLeave": func(s string) (interface{}, error) {
		return msgsvr.NewKeyLeave(s)
	},

	// KeyRequestLeave - msgcli\keyrequestleave.go
	"KeyRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewKeyRequestLeave(s)
	},

	// KeySendKey - msgcli\keysendkey.go
	"KeySendKey": func(s string) (interface{}, error) {
		return msgcli.NewKeySendKey(s)
	},

	// MountCastrate - msgcli\mountcastrate.go
	"MountCastrate": func(s string) (interface{}, error) {
		return msgcli.NewMountCastrate(s)
	},

	// MountData - msgsvr\mountdata.go
	"MountData": func(s string) (interface{}, error) {
		return msgsvr.NewMountData(s)
	},

	// MountEquipError - msgsvr\mountequiperror.go
	"MountEquipError": func(s string) (interface{}, error) {
		return msgsvr.NewMountEquipError(s)
	},

	// MountEquipSuccess - msgsvr\mountequipsuccess.go
	"MountEquipSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewMountEquipSuccess(s)
	},

	// MountFree - msgcli\mountfree.go
	"MountFree": func(s string) (interface{}, error) {
		return msgcli.NewMountFree(s)
	},

	// MountLeave - msgsvr\mountleave.go
	"MountLeave": func(s string) (interface{}, error) {
		return msgsvr.NewMountLeave(s)
	},

	// MountMountPark - msgsvr\mountmountpark.go
	"MountMountPark": func(s string) (interface{}, error) {
		return msgsvr.NewMountMountPark(s)
	},

	// MountMountParkBuy - msgsvr\mountmountparkbuy.go
	"MountMountParkBuy": func(s string) (interface{}, error) {
		return msgsvr.NewMountMountParkBuy(s)
	},

	// MountMountParkSell - msgcli\mountmountparksell.go
	"MountMountParkSell": func(s string) (interface{}, error) {
		return msgcli.NewMountMountParkSell(s)
	},

	// MountName - msgsvr\mountname.go
	"MountName": func(s string) (interface{}, error) {
		return msgsvr.NewMountName(s)
	},

	// MountParkMountData - msgcli\mountparkmountdata.go
	"MountParkMountData": func(s string) (interface{}, error) {
		return msgcli.NewMountParkMountData(s)
	},

	// MountRemoveObjectInPark - msgcli\mountremoveobjectinpark.go
	"MountRemoveObjectInPark": func(s string) (interface{}, error) {
		return msgcli.NewMountRemoveObjectInPark(s)
	},

	// MountRename - msgcli\mountrename.go
	"MountRename": func(s string) (interface{}, error) {
		return msgcli.NewMountRename(s)
	},

	// MountRequestData - msgcli\mountrequestdata.go
	"MountRequestData": func(s string) (interface{}, error) {
		return msgcli.NewMountRequestData(s)
	},

	// MountRequestLeave - msgcli\mountrequestleave.go
	"MountRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewMountRequestLeave(s)
	},

	// MountRequestMountParkBuy - msgcli\mountrequestmountparkbuy.go
	"MountRequestMountParkBuy": func(s string) (interface{}, error) {
		return msgcli.NewMountRequestMountParkBuy(s)
	},

	// MountRide - msgcli\mountride.go
	"MountRide": func(s string) (interface{}, error) {
		return msgcli.NewMountRide(s)
	},

	// MountRidingState - msgsvr\mountridingstate.go
	"MountRidingState": func(s string) (interface{}, error) {
		return msgsvr.NewMountRidingState(s)
	},

	// MountSetXP - msgcli\mountsetxp.go
	"MountSetXP": func(s string) (interface{}, error) {
		return msgcli.NewMountSetXP(s)
	},

	// MountUnequip - msgsvr\mountunequip.go
	"MountUnequip": func(s string) (interface{}, error) {
		return msgsvr.NewMountUnequip(s)
	},

	// MountXP - msgsvr\mountxp.go
	"MountXP": func(s string) (interface{}, error) {
		return msgsvr.NewMountXP(s)
	},

	// PartyAccept - msgsvr\partyaccept.go
	"PartyAccept": func(s string) (interface{}, error) {
		return msgsvr.NewPartyAccept(s)
	},

	// PartyAcceptInvitation - msgcli\partyacceptinvitation.go
	"PartyAcceptInvitation": func(s string) (interface{}, error) {
		return msgcli.NewPartyAcceptInvitation(s)
	},

	// PartyCreateError - msgsvr\partycreateerror.go
	"PartyCreateError": func(s string) (interface{}, error) {
		return msgsvr.NewPartyCreateError(s)
	},

	// PartyCreateSuccess - msgsvr\partycreatesuccess.go
	"PartyCreateSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewPartyCreateSuccess(s)
	},

	// PartyFollowAll - msgcli\partyfollowall.go
	"PartyFollowAll": func(s string) (interface{}, error) {
		return msgcli.NewPartyFollowAll(s)
	},

	// PartyFollowError - msgsvr\partyfollowerror.go
	"PartyFollowError": func(s string) (interface{}, error) {
		return msgsvr.NewPartyFollowError(s)
	},

	// PartyFollowSuccess - msgsvr\partyfollowsuccess.go
	"PartyFollowSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewPartyFollowSuccess(s)
	},

	// PartyInvite - msgcli\partyinvite.go
	"PartyInvite": func(s string) (interface{}, error) {
		return msgcli.NewPartyInvite(s)
	},

	// PartyInviteError - msgsvr\partyinviteerror.go
	"PartyInviteError": func(s string) (interface{}, error) {
		return msgsvr.NewPartyInviteError(s)
	},

	// PartyInviteSuccess - msgsvr\partyinvitesuccess.go
	"PartyInviteSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewPartyInviteSuccess(s)
	},

	// PartyLeader - msgsvr\partyleader.go
	"PartyLeader": func(s string) (interface{}, error) {
		return msgsvr.NewPartyLeader(s)
	},

	// PartyLeave - msgsvr\partyleave.go
	"PartyLeave": func(s string) (interface{}, error) {
		return msgsvr.NewPartyLeave(s)
	},

	// PartyMovement - msgsvr\partymovement.go
	"PartyMovement": func(s string) (interface{}, error) {
		return msgsvr.NewPartyMovement(s)
	},

	// PartyRefuse - msgsvr\partyrefuse.go
	"PartyRefuse": func(s string) (interface{}, error) {
		return msgsvr.NewPartyRefuse(s)
	},

	// PartyRefuseInvitation - msgcli\partyrefuseinvitation.go
	"PartyRefuseInvitation": func(s string) (interface{}, error) {
		return msgcli.NewPartyRefuseInvitation(s)
	},

	// PartyRequestFollow - msgcli\partyrequestfollow.go
	"PartyRequestFollow": func(s string) (interface{}, error) {
		return msgcli.NewPartyRequestFollow(s)
	},

	// PartyRequestLeave - msgcli\partyrequestleave.go
	"PartyRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewPartyRequestLeave(s)
	},

	// PartyWhere - msgcli\partywhere.go
	"PartyWhere": func(s string) (interface{}, error) {
		return msgcli.NewPartyWhere(s)
	},

	// QuestGetList - msgcli\questgetlist.go
	"QuestGetList": func(s string) (interface{}, error) {
		return msgcli.NewQuestGetList(s)
	},

	// QuestGetStep - msgcli\questgetstep.go
	"QuestGetStep": func(s string) (interface{}, error) {
		return msgcli.NewQuestGetStep(s)
	},

	// QuestsList - msgsvr\questslist.go
	"QuestsList": func(s string) (interface{}, error) {
		return msgsvr.NewQuestsList(s)
	},

	// QuestsStep - msgsvr\questsstep.go
	"QuestsStep": func(s string) (interface{}, error) {
		return msgsvr.NewQuestsStep(s)
	},

	// SpecializationChange - msgsvr\specializationchange.go
	"SpecializationChange": func(s string) (interface{}, error) {
		return msgsvr.NewSpecializationChange(s)
	},

	// SpecializationSet - msgsvr\specializationset.go
	"SpecializationSet": func(s string) (interface{}, error) {
		return msgsvr.NewSpecializationSet(s)
	},

	// SpellsBoost - msgcli\spellsboost.go
	"SpellsBoost": func(s string) (interface{}, error) {
		return msgcli.NewSpellsBoost(s)
	},

	// SpellsChangeOption - msgsvr\spellschangeoption.go
	"SpellsChangeOption": func(s string) (interface{}, error) {
		return msgsvr.NewSpellsChangeOption(s)
	},

	// SpellsForget - msgcli\spellsforget.go
	"SpellsForget": func(s string) (interface{}, error) {
		return msgcli.NewSpellsForget(s)
	},

	// SpellsList - msgsvr\spellslist.go
	"SpellsList": func(s string) (interface{}, error) {
		return msgsvr.NewSpellsList(s)
	},

	// SpellsMoveToUsed - msgcli\spellsmovetoused.go
	"SpellsMoveToUsed": func(s string) (interface{}, error) {
		return msgcli.NewSpellsMoveToUsed(s)
	},

	// SpellsSpellBoost - msgsvr\spellsspellboost.go
	"SpellsSpellBoost": func(s string) (interface{}, error) {
		return msgsvr.NewSpellsSpellBoost(s)
	},

	// SpellsSpellForgetClose - msgsvr\spellsspellforgetclose.go
	"SpellsSpellForgetClose": func(s string) (interface{}, error) {
		return msgsvr.NewSpellsSpellForgetClose(s)
	},

	// SpellsSpellForgetShow - msgsvr\spellsspellforgetshow.go
	"SpellsSpellForgetShow": func(s string) (interface{}, error) {
		return msgsvr.NewSpellsSpellForgetShow(s)
	},

	// SpellsUpgradeSpellError - msgsvr\spellsupgradespellerror.go
	"SpellsUpgradeSpellError": func(s string) (interface{}, error) {
		return msgsvr.NewSpellsUpgradeSpellError(s)
	},

	// SpellsUpgradeSpellSuccess - msgsvr\spellsupgradespellsuccess.go
	"SpellsUpgradeSpellSuccess": func(s string) (interface{}, error) {
		return msgsvr.NewSpellsUpgradeSpellSuccess(s)
	},

	// StoragesListAdd - msgsvr\storageslistadd.go
	"StoragesListAdd": func(s string) (interface{}, error) {
		return msgsvr.NewStoragesListAdd(s)
	},

	// StoragesListRemove - msgsvr\storageslistremove.go
	"StoragesListRemove": func(s string) (interface{}, error) {
		return msgsvr.NewStoragesListRemove(s)
	},

	// StoragesLockedProperty - msgsvr\storageslockedproperty.go
	"StoragesLockedProperty": func(s string) (interface{}, error) {
		return msgsvr.NewStoragesLockedProperty(s)
	},

	// SubareasAlignmentModification - msgsvr\subareasalignmentmodification.go
	"SubareasAlignmentModification": func(s string) (interface{}, error) {
		return msgsvr.NewSubareasAlignmentModification(s)
	},

	// SubareasList - msgsvr\subareaslist.go
	"SubareasList": func(s string) (interface{}, error) {
		return msgsvr.NewSubareasList(s)
	},

	// SubwayCreate - msgsvr\subwaycreate.go
	"SubwayCreate": func(s string) (interface{}, error) {
		return msgsvr.NewSubwayCreate(s)
	},

	// SubwayLeave - msgsvr\subwayleave.go
	"SubwayLeave": func(s string) (interface{}, error) {
		return msgsvr.NewSubwayLeave(s)
	},

	// SubwayPrismCreate - msgsvr\subwayprismcreate.go
	"SubwayPrismCreate": func(s string) (interface{}, error) {
		return msgsvr.NewSubwayPrismCreate(s)
	},

	// SubwayPrismLeave - msgsvr\subwayprismleave.go
	"SubwayPrismLeave": func(s string) (interface{}, error) {
		return msgsvr.NewSubwayPrismLeave(s)
	},

	// SubwayPrismUse - msgcli\subwayprismuse.go
	"SubwayPrismUse": func(s string) (interface{}, error) {
		return msgcli.NewSubwayPrismUse(s)
	},

	// SubwayRequestLeave - msgcli\subwayrequestleave.go
	"SubwayRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewSubwayRequestLeave(s)
	},

	// SubwayRequestPrismLeave - msgcli\subwayrequestprismleave.go
	"SubwayRequestPrismLeave": func(s string) (interface{}, error) {
		return msgcli.NewSubwayRequestPrismLeave(s)
	},

	// SubwayUse - msgcli\subwayuse.go
	"SubwayUse": func(s string) (interface{}, error) {
		return msgcli.NewSubwayUse(s)
	},

	// SubwayUseError - msgsvr\subwayuseerror.go
	"SubwayUseError": func(s string) (interface{}, error) {
		return msgsvr.NewSubwayUseError(s)
	},

	// TutorialCreate - msgsvr\tutorialcreate.go
	"TutorialCreate": func(s string) (interface{}, error) {
		return msgsvr.NewTutorialCreate(s)
	},

	// TutorialEnd - msgcli\tutorialend.go
	"TutorialEnd": func(s string) (interface{}, error) {
		return msgcli.NewTutorialEnd(s)
	},

	// TutorialGameBegin - msgsvr\tutorialgamebegin.go
	"TutorialGameBegin": func(s string) (interface{}, error) {
		return msgsvr.NewTutorialGameBegin(s)
	},

	// TutorialShowTip - msgsvr\tutorialshowtip.go
	"TutorialShowTip": func(s string) (interface{}, error) {
		return msgsvr.NewTutorialShowTip(s)
	},

	// WaypointsCreate - msgsvr\waypointscreate.go
	"WaypointsCreate": func(s string) (interface{}, error) {
		return msgsvr.NewWaypointsCreate(s)
	},

	// WaypointsLeave - msgsvr\waypointsleave.go
	"WaypointsLeave": func(s string) (interface{}, error) {
		return msgsvr.NewWaypointsLeave(s)
	},

	// WaypointsRequestLeave - msgcli\waypointsrequestleave.go
	"WaypointsRequestLeave": func(s string) (interface{}, error) {
		return msgcli.NewWaypointsRequestLeave(s)
	},

	// WaypointsUse - msgcli\waypointsuse.go
	"WaypointsUse": func(s string) (interface{}, error) {
		return msgcli.NewWaypointsUse(s)
	},

	// WaypointsUseError - msgsvr\waypointsuseerror.go
	"WaypointsUseError": func(s string) (interface{}, error) {
		return msgsvr.NewWaypointsUseError(s)
	},

}

// GetMessageNames returns all registered message names
func GetMessageNames() []string {
	names := make([]string, 0, len(Registry))
	for name := range Registry {
		names = append(names, name)
	}
	return names
}
