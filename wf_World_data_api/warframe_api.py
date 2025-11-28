import requests
import json
import os
from datetime import datetime, timezone

# 名称映射文件路径
MAPPING_FILE = "wfdata.json"
NODE_MAPPING_FILE = "node.json"  # 新增节点映射文件路径

def load_name_mappings():
    """加载名称映射"""
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 如果文件不存在，返回空映射
        return {
            "missions": {},
            "factions": {},
            "bosses": {},
            "syndicates": {},
            "nodes": {}  # 新增节点映射
        }

def load_node_mappings():
    """加载节点映射"""
    if os.path.exists(NODE_MAPPING_FILE):
        with open(NODE_MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"⚠️节点映射文件 {NODE_MAPPING_FILE} 不存在")
        return {}

def save_name_mappings(mappings):
    """保存名称映射"""
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, ensure_ascii=False, indent=2)

# 加载名称映射
name_mappings = load_name_mappings()
node_mappings = load_node_mappings()

# 将节点映射合并到主映射中
if node_mappings:
    name_mappings['nodes'] = node_mappings

def extract_modifier_name(modifier_key):
    """从修饰符键中提取可读的裂隙等级名称"""
    if not modifier_key:
        return "未知等级"
    
    # 从映射文件中查找
    if modifier_key in name_mappings.get('Modifier', {}):
        return name_mappings['Modifier'][modifier_key]
    
    # 如果映射文件中没有，返回原始键（清理一下显示）
    clean_key = modifier_key.replace('Void', '').replace('Storm', '风暴')
    return clean_key

def fetch_warframe_data():
    """获取Warframe所有实时数据并直接打印"""
    try:
        # Warframe官方API端点
        url = "https://content.warframe.com/dynamic/worldState.php"
        
        print("🔄正在获取Warframe实时数据...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 清屏并显示所有数据
        print("\n" + "="*20)
        print("🎮WARFRAME 实时数据监控")
        print("="*20)
        print(f"📅更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*20)
        
        # 显示所有数据模块
        display_alerts(data)
        display_invasions(data)
        display_events(data)
        display_sorties(data)
        display_void_fissures(data)
        display_void_trader(data)
        display_syndicate_missions(data)
        display_open_world_bounties(data)
        display_nightwave(data)
        #display_flash_sales(data)
        #display_daily_deals(data)
        display_railjack(data)
        display_archon_hunt(data)
        
        print("="*20)
        print("✅数据获取完成！")
        
        return data
        
    except Exception as e:
        print(f"❌发生错误: {e}")
        return None

def extract_node_name(node_key):
    """从节点映射中提取节点名称"""
    if node_key in name_mappings.get('nodes', {}):
        return name_mappings['nodes'][node_key]
    return node_key

def load_challenge_mapping():
    """加载挑战名称映射"""
    try:
        with open('dict_zh.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ 警告：dict_zh.json 文件未找到，将使用原始路径显示")
        return {}
    except Exception as e:
        print(f"⚠️ 警告：加载 dict_zh.json 时出错: {e}")
        return {}

def extract_challenge_name(challenge_path, challenge_mapping):
    """从映射中提取挑战名称"""
    if challenge_path in challenge_mapping:
        return challenge_mapping[challenge_path]
    else:
        # 如果映射中没有找到，尝试从路径中提取最后一部分作为备用
        parts = challenge_path.split('/')
        return parts[-1] if parts else challenge_path

def display_nightwave(data):
    """显示午夜电波信息（使用dict_zh.json映射）"""
    # 加载挑战名称映射
    challenge_mapping = load_challenge_mapping()
    
    season_info = data.get('SeasonInfo', {})
    
    print(f"\n🌙午夜电波:")
    
    if season_info:
        season = season_info.get('Season', 0)
        phase = season_info.get('Phase', 0)
        active_challenges = season_info.get('ActiveChallenges', [])
        
        daily_challenges = [c for c in active_challenges if c.get('Daily')]
        weekly_challenges = [c for c in active_challenges if not c.get('Daily')]
        
        print(f"   • 赛季: {season}")
        print(f"   • 阶段: {phase}")
        print(f"   • 每日挑战: {len(daily_challenges)} 个")
        
        if daily_challenges:
            for i, challenge in enumerate(daily_challenges, 1):
                challenge_path = challenge.get('Challenge', '')
                challenge_name = extract_challenge_name(challenge_path, challenge_mapping)
                print(f"      {i}. {challenge_name}")
        else:
            print("📭无每日挑战")
        
        print(f"   • 每周挑战: {len(weekly_challenges)} 个")
        
        if weekly_challenges:
            for i, challenge in enumerate(weekly_challenges, 1):
                challenge_path = challenge.get('Challenge', '')
                challenge_name = extract_challenge_name(challenge_path, challenge_mapping)
                print(f"      {i}. {challenge_name}")
        else:
            print("📭无每周挑战")
        
        # 显示映射统计信息
        mapped_count = sum(1 for c in active_challenges if c.get('Challenge', '') in challenge_mapping)
        total_count = len(active_challenges)
        print(f"   • 映射状态: {mapped_count}/{total_count} 个挑战已映射")
        
    else:
        print("📭午夜电波信息不可用")

def display_syndicate_missions(data):
    """显示集团任务信息"""
    try:
        syndicates = data.get('SyndicateMissions', [])
        
        print(f"\n🏛️ 集团任务:")
        print(f"   • 总集团任务: {len(syndicates)}")
        
        if not syndicates:
            print("📭当前无集团任务")
            return
        
        main_syndicates = ['SteelMeridian', 'Arbiters', 'CephalonSuda', 'Perrin', 'RedVeil', 'NewLoka']
        active_syndicates = []
        
        for syndicate in syndicates:
            if not isinstance(syndicate, dict):
                continue
                
            tag = syndicate.get('Tag', '')
            if any(main in tag for main in main_syndicates):
                active_syndicates.append(syndicate)
        
        print(f"   • 活跃集团: {len(active_syndicates)}")
        
        if not active_syndicates:
            print("📭当前无活跃集团任务")
            return
            
        # 显示每个集团的任务列表
        for syndicate in active_syndicates:
            tag = syndicate.get('Tag', '')
            syndicate_name = extract_name(tag.replace('Syndicate', '').replace('_', ' ').strip(), 'syndicates')
            node_ids = syndicate.get('Nodes', [])
            
            if not node_ids or not isinstance(node_ids, list):
                print(f"   • {syndicate_name}: 0 个任务")
                continue
                
            print(f"   • {syndicate_name}: {len(node_ids)} 个任务")
            
            # 使用节点映射显示可读的节点名称
            if node_ids:
                for i, node_id in enumerate(node_ids, 1):
                    node_name = extract_node_name(node_id)
                    print(f"      {i}. {node_name}")
            else:
                print("      无可用节点信息")
            
            print()  # 空行分隔不同集团
                
    except Exception as e:
        print(f"❌处理集团任务时出错: {e}")
        import traceback
        print(f"   详细错误: {traceback.format_exc()}")

def display_open_world_bounties(data):
    """显示开放世界赏金任务（使用两级映射）"""
    print(f"\n🌍开放世界赏金:")
    
    # 加载两级映射
    export_bounties = {}
    dict_zh = {}
    
    try:
        # 加载第一级映射（ExportBounties.json）
        with open('ExportBounties.json', 'r', encoding='utf-8') as f:
            export_bounties = json.load(f)
        
        # 加载第二级映射（dict_zh.json）
        with open('dict_zh.json', 'r', encoding='utf-8') as f:
            dict_zh = json.load(f)
    except Exception as e:
        print(f"⚠️加载映射文件时出错: {e}")
        # 如果文件加载失败，使用您提供的示例数据
    
    locations = [
        ('CetusSyndicate', '地球希图斯'),
        ('SolarisSyndicate', '金星福尔图娜'), 
        ('EntratiSyndicate', '火卫二殁世幽都')
    ]
    
    has_bounties = False
    
    for tag, name in locations:
        bounties = [s for s in data.get('SyndicateMissions', []) if s.get('Tag') == tag]
        if bounties:
            jobs = bounties[0].get('Jobs', [])
            print(f"   • {name}: {len(jobs)} 个赏金")
            
            # 显示所有赏金任务，使用两级映射
            for i, job in enumerate(jobs, 1):
                job_type = job.get('jobType', '')
                masteryReq = job.get('masteryReq', 0)
                min_level = job.get('minEnemyLevel', 0)
                max_level = job.get('maxEnemyLevel', 0)
                
                # 两级映射：jobType -> ExportBounties -> dict_zh
                bounty_name = map_bounty_name(job_type, export_bounties, dict_zh)
                
                print(f"      {i}. 等级 {min_level}-{max_level} | {bounty_name} | 精通等级: {masteryReq}")
            
            has_bounties = True
            print()  # 空行分隔不同地点
    
    if not has_bounties:
        print("📭📭当前无赏金任务")

def map_bounty_name(job_type, export_bounties, dict_zh):
    """使用两级映射获取赏金任务的中文名称"""
    if not job_type:
        return "未知赏金"
    
    # 第一级映射：从jobType到语言键
    language_key = export_bounties.get(job_type, "")
    if not language_key:
        # 如果第一级映射失败，尝试直接使用jobType的最后部分
        parts = job_type.split('/')
        return parts[-1] if parts else job_type
    
    # 第二级映射：从语言键到中文名称
    chinese_name = dict_zh.get(language_key, "")
    if chinese_name:
        return chinese_name
    
    # 如果第二级映射失败，返回语言键的最后部分
    parts = language_key.split('/')
    return parts[-1] if parts else language_key

def extract_name(key, category):
    """从映射中提取名称"""
    if key in name_mappings.get(category, {}):
        return name_mappings[category][key]
    return key

def display_alerts(data):
    """显示警报信息"""
    alerts = data.get('Alerts', [])
    active_alerts = [alert for alert in alerts if is_active(alert)]
    
    print(f"🚨警报信息:")
    print(f"   • 总数: {len(alerts)}")
    print(f"   • 活跃: {len(active_alerts)}")
    
    if active_alerts:
        for i, alert in enumerate(active_alerts, 1):
            mission_info = alert.get('MissionInfo', {})
            mission_type = extract_name(mission_info.get('missionType', '未知'), 'missions')
            faction = extract_name(mission_info.get('faction', '未知'), 'factions')
            reward = mission_info.get('missionReward', {}).get('credits', 0)
            location_key = alert.get('MissionInfo', {}).get('location', '未知地点')
            location = extract_node_name(location_key)  # 使用节点映射
            print(f"   {i}. {mission_type} | {faction} | {location} | 奖励: {reward} 现金")
    else:
        print("📭当前无活跃警报")

def display_invasions(data):
    """显示入侵信息"""
    invasions = data.get('Invasions', [])
    active_invasions = [inv for inv in invasions if not inv.get('Completed', False)]
    completed_invasions = [inv for inv in invasions if inv.get('Completed', False)]
    
    print(f"\n⚔️入侵信息:")
    print(f"   • 总数: {len(invasions)}")
    print(f"   • 进行中: {len(active_invasions)}")
    print(f"   • 已完成: {len(completed_invasions)}")
    
    if active_invasions:
        for i, invasion in enumerate(active_invasions, 1):
            node_key = invasion.get('Node', '未知节点')
            node = extract_node_name(node_key)  # 使用节点映射
            faction = extract_name(invasion.get('Faction', '未知'), 'factions')
            count = invasion.get('Count', 0)
            goal = invasion.get('Goal', 0)
            progress = (abs(count) / goal * 100) if goal > 0 else 0
            print(f"   {i}. {node} | {faction} | 进度: {progress:.1f}%")
    else:
        print("📭当前无进行中入侵")

def display_events(data):
    """显示新闻信息"""
    events = data.get('Events', [])
    
    # 只筛选有中文描述且活跃的新闻
    chinese_active_events = []
    for event in events:
        if is_active_event(event):
            messages = event.get('Messages', [])
            # 检查是否有中文描述
            for msg in messages:
                if msg.get('LanguageCode') == 'zh':
                    chinese_active_events.append(event)
                    break
    
    print(f"\n🎪新闻信息:")
    print(f"   • 总数: {len(events)}")
    print(f"   • 有中文描述的新闻: {len(chinese_active_events)}")
    
    if chinese_active_events:
        for i, event in enumerate(chinese_active_events, 1):
            messages = event.get('Messages', [])
            event_name = "无描述"
            
            # 提取中文描述
            for msg in messages:
                if msg.get('LanguageCode') == 'zh':
                    event_name = msg.get('Message', '无描述')[:40]
                    break
            
            print(f"   {i}. {event_name}...")
    else:
        print("📭当前无中文新闻")

def display_sorties(data):
    """显示突击任务信息"""
    sorties = data.get('Sorties', [])
    
    print(f"\n🎯突击任务:")
    if sorties:
        sortie = sorties[0]
        boss = extract_name(sortie.get('Boss', '未知'), 'bosses')
        variants = sortie.get('Variants', [])
        
        print(f"   • BOSS: {boss}")
        print(f"   • 阶段数: {len(variants)}")
        
        for i, variant in enumerate(variants, 1):
            mission_type = extract_name(variant.get('missionType', '未知'), 'missions')
            modifier = variant.get('modifierType', '无').replace('SORTIE_MODIFIER_', '')
            node_key = variant.get('node', '未知地点')
            node = extract_node_name(node_key)  # 使用节点映射
            print(f"   {i}. {mission_type} - {modifier} | {node}")
    else:
        print("📭今日无突击任务")

def display_void_fissures(data):
    """显示裂隙信息"""
    active_missions = data.get('ActiveMissions', [])
    void_fissures = [m for m in active_missions if m.get('Modifier', '').startswith('Void')]
    
    print(f"\n🌀虚空裂隙:")
    print(f"   • 活跃裂隙: {len(void_fissures)}")
    
    if void_fissures:
        # 按裂隙等级分组显示
        fissures_by_tier = {}
        for fissure in void_fissures:
            tier = fissure.get('Modifier', 'VoidT?')
            if tier not in fissures_by_tier:
                fissures_by_tier[tier] = []
            fissures_by_tier[tier].append(fissure)
        
        # 按等级排序显示
        sorted_tiers = sorted(fissures_by_tier.keys())
        
        for tier in sorted_tiers:
            fissures = fissures_by_tier[tier]
            tier_name = extract_modifier_name(tier)  # 使用裂隙等级映射
            mission_type = extract_name(fissures[0].get('MissionType', '未知'), 'missions') if fissures else '未知'
            
            print(f"   • {tier_name} : {len(fissures)} 个")
            
            # 显示该等级下的所有裂隙
            for i, fissure in enumerate(fissures, 1):
                node_key = fissure.get('Node', '未知节点')
                node = extract_node_name(node_key)  # 使用节点映射
                mission_type = extract_name(fissure.get('MissionType', '未知'), 'missions')
                
                # 获取剩余时间
                expiry = fissure.get('Expiry', {})
                time_remaining = "未知"
                if isinstance(expiry, dict) and '$date' in expiry:
                    expiry_ms = expiry['$date'].get('$numberLong', 0)
                    if expiry_ms:
                        expiry_time = datetime.fromtimestamp(int(expiry_ms) / 1000, tz=timezone.utc)
                        current_time = datetime.now(timezone.utc)
                        time_remaining = expiry_time - current_time
                        if time_remaining.days > 0:
                            time_str = f"{time_remaining.days}天{time_remaining.seconds//3600}时"
                        else:
                            hours = time_remaining.seconds // 3600
                            minutes = (time_remaining.seconds % 3600) // 60
                            time_str = f"{hours}时{minutes}分"
                
                print(f"      {i}. {node} - {mission_type} - 剩余: {time_str}")
            
            print()  # 空行分隔不同等级
    else:
        print("📭当前无活跃裂隙")

def display_void_trader(data):
    """显示虚空商人信息"""
    traders = data.get('VoidTraders', [])
    
    print(f"\n👑虚空商人 Baro Ki'Teer:")
    
    if traders:
        trader = traders[0]
        activation = trader.get('Activation', {})
        expiry = trader.get('Expiry', {})
        
        activation_ms = activation.get('$date', {}).get('$numberLong', 0) if isinstance(activation, dict) else 0
        expiry_ms = expiry.get('$date', {}).get('$numberLong', 0) if isinstance(expiry, dict) else 0
        
        if activation_ms and expiry_ms:
            activation_time = datetime.fromtimestamp(int(activation_ms) / 1000, tz=timezone.utc)
            expiry_time = datetime.fromtimestamp(int(expiry_ms) / 1000, tz=timezone.utc)
            current_time = datetime.now(timezone.utc)
            
            if current_time < activation_time:
                time_until = activation_time - current_time
                print(f"   • 状态:🕐即将到来")
                print(f"   • 到达时间: {activation_time.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   • 距离到达: {time_until.days}天 {time_until.seconds//3600}小时")
                
            elif activation_time <= current_time < expiry_time:
                time_remaining = expiry_time - current_time
                location_key = trader.get('Node', '未知地点').replace('HUB', '中继站')
                location = extract_node_name(location_key)  # 使用节点映射
                manifest = trader.get('Manifest', [])
                
                print(f"   • 状态: ✅ 正在访问")
                print(f"   • 位置: {location}")
                print(f"   • 剩余时间: {time_remaining.days}天 {time_remaining.seconds//3600}小时")
                print(f"   • 携带商品: {len(manifest)} 件")
            else:
                time_since = current_time - expiry_time
                print(f"   • 状态:❌ 已离开")
                print(f"   • 离开时间: {expiry_time.strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   • 已离开: {time_since.days} 天")
    else:
        print("📭暂无虚空商人信息")

'''
def display_flash_sales(data):
    """显示促销商品信息"""
    flash_sales = data.get('FlashSales', [])
    active_sales = [sale for sale in flash_sales if sale.get('Discount', 0) > 0]
    
    print(f"\n🛍🛍️促销商品:")
    print(f"   • 总促销: {len(flash_sales)}")
    print(f"   • 有折扣: {len(active_sales)}")
    
    if active_sales:
        for i, sale in enumerate(active_sales, 1):
            item_type = sale.get('TypeName', '未知商品').split('/')[-1]
            discount = sale.get('Discount', 0)
            print(f"   {i}. {item_type} - {discount}% 折扣")
    else:
        print("📭当前无促销商品")

def display_daily_deals(data):
    """显示每日特价"""
    daily_deals = data.get('DailyDeals', [])
    
    print(f"\n💎每日特价:")
    print(f"   • 可用特价: {len(daily_deals)}")
    
    if daily_deals:
        for i, deal in enumerate(daily_deals, 1):
            item_name = deal.get('StoreItem', '未知商品').split('/')[-1]
            discount = deal.get('Discount', 0)
            remaining = deal.get('AmountTotal', 0) - deal.get('AmountSold', 0)
            print(f"   {i}. {item_name} - {discount}% 折扣 (剩余: {remaining})")
    else:
        print("📭当前无每日特价")
'''

def display_railjack(data):
    """显示九重天信息"""
    void_storms = data.get('VoidStorms', [])
    
    print(f"\n🚀九重天:")
    print(f"   • 虚空风暴: {len(void_storms)} 个")
    
    if void_storms:
        # 按风暴等级分组显示
        storms_by_tier = {}
        for storm in void_storms:
            tier = storm.get('ActiveMissionTier', '未知等级')
            if tier not in storms_by_tier:
                storms_by_tier[tier] = []
            storms_by_tier[tier].append(storm)
        
        # 按等级排序显示
        sorted_tiers = sorted(storms_by_tier.keys())
        
        for tier in sorted_tiers:
            storms = storms_by_tier[tier]
            tier_name = extract_modifier_name(tier)  # 使用裂隙等级映射
            
            print(f"   • {tier_name}: {len(storms)} 个")
            
            for i, storm in enumerate(storms, 1):
                node_key = storm.get('Node', '未知节点')
                node = extract_node_name(node_key)  # 使用节点映射
                print(f"      {i}. {node}")
            
            print()  # 空行分隔不同等级

def display_archon_hunt(data):
    """显示刺杀执行官信息"""
    try:
        # 从 LiteSorties 中获取执行官数据
        lite_sorties = data.get('LiteSorties', [])
        
        print(f"\n👹刺杀执行官:")
        
        # 查找执行官任务（通过 Boss 字段包含 ARCHON 或特定执行官名称）
        archon_hunt = None
        for sortie in lite_sorties:
            boss = sortie.get('Boss', '')
            # 检查是否是执行官任务
            if any(archon_keyword in boss for archon_keyword in ['ARCHON', 'NIRA', 'AMAR', 'BOREAL']):
                archon_hunt = sortie
                break
        
        if archon_hunt:
            # 提取执行官信息
            boss = archon_hunt.get('Boss', '未知执行官')
            boss_name = extract_archon_name(boss)
            
            # 提取任务信息（从 Missions 字段）
            missions = archon_hunt.get('Missions', [])
            
            # 获取激活和过期时间
            activation = archon_hunt.get('Activation', {})
            expiry = archon_hunt.get('Expiry', {})
            
            activation_ms = activation.get('$date', {}).get('$numberLong', 0) if isinstance(activation, dict) else 0
            expiry_ms = expiry.get('$date', {}).get('$numberLong', 0) if isinstance(expiry, dict) else 0
            
            print(f"   • 执行官: {boss_name}")
            print(f"   • 阶段数: {len(missions)}")
            
            if activation_ms and expiry_ms:
                activation_time = datetime.fromtimestamp(int(activation_ms) / 1000, tz=timezone.utc)
                expiry_time = datetime.fromtimestamp(int(expiry_ms) / 1000, tz=timezone.utc)
                current_time = datetime.now(timezone.utc)
                
                if current_time < activation_time:
                    time_until = activation_time - current_time
                    print(f"   • 状态: 🕐 即将开始")
                    print(f"   • 开始时间: {activation_time.strftime('%Y-%m-%d %H:%M UTC')}")
                    print(f"   • 距离开始: {time_until.days}天 {time_until.seconds//3600}小时")
                elif activation_time <= current_time < expiry_time:
                    time_remaining = expiry_time - current_time
                    print(f"   • 状态: ✅ 进行中")
                    print(f"   • 剩余时间: {time_remaining.days}天 {time_remaining.seconds//3600}小时")
                else:
                    print(f"   • 状态: ❌ 已结束")
            
            if missions:
                for i, mission in enumerate(missions, 1):
                    mission_type = extract_name(mission.get('missionType', '未知'), 'missions')
                    node_key = mission.get('node', '未知地点')
                    node_name = extract_node_name(node_key)
                    
                    print(f"   {i}. {node_name} - {mission_type}")
            else:
                print("📭无任务信息")
        
        else:
            print("📭当前无执行官任务")
                
    except Exception as e:
        print(f"❌处理执行官信息时出错: {e}")
        import traceback
        print(f"   详细错误: {traceback.format_exc()}")

def extract_archon_name(archon_key):
    """从执行官键中提取可读的执行官名称"""
    if not archon_key:
        return "未知执行官"
    
    # 从映射中查找（使用name_mappings中的bosses映射）
    if archon_key in name_mappings.get('bosses', {}):
        return name_mappings['bosses'][archon_key]
    
    # 如果映射中没有，返回清理后的名称
    clean_name = archon_key.replace('SORTIE_BOSS_', '').replace('ARCHON_', '')
    return clean_name


def is_active(item):
    """检查项目是否活跃"""
    expiry = item.get('Expiry', {})
    if isinstance(expiry, dict) and '$date' in expiry:
        expiry_ms = expiry['$date'].get('$numberLong', 0)
        if expiry_ms:
            expiry_time = datetime.fromtimestamp(int(expiry_ms) / 1000, tz=timezone.utc)
            return datetime.now(timezone.utc) < expiry_time
    return True

def is_active_event(event):
    """检查活动是否活跃"""
    return 'EventEndDate' in event or 'Date' in event

# 直接运行时就打印所有数据
if __name__ == "__main__":
    fetch_warframe_data()