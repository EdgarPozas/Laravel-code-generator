<?php

namespace App;

use Illuminate\Notifications\Notifiable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Contracts\Auth\Authenticatable;

class #name# extends Model implements Authenticatable {
    use \Illuminate\Auth\Authenticatable;
    use Notifiable;

	protected $fillable=[#fillable#];
	protected $hidden=[#hidden#];
	protected $casts=[#casts#];
#if "#primary#"!=""
	protected $primaryKey = "#primary#";
#endif
	public $timestamps=#timestamps#;
#foreign#
}